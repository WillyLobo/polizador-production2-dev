import json
from collections import defaultdict

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.gis.db.models.functions import Transform
from django.contrib.gis.geos import Polygon
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from gdu.matching import normalizar_expediente
from gdu.models import (
    Barrios,
    Catastrourbano,
    Expropiaciones,
    Localidad,
    ObraContratacion,
    Parcela,
    PlanoMensura,
    ViviendaDispersa,
    Viviendas,
    ViviendasParaEscriturar,
)

MAP_SRID = 3857  # como la manda ol/loadingstrategy/bbox, para el filtro espacial
GEOJSON_SRID = 4326  # GeoJSON (RFC 7946) siempre es WGS84; ol.format.GeoJSON asume esto al reproyectar
MAX_FEATURES_POR_CAPA = 3000


def _obras_por_expediente():
    """
    {expediente normalizado de la contratación: [(obra_id, obra_nombre), ...]} para poder
    resolver, a partir del campo `expediente` que ya traen las vistas del mapa
    (Viviendas/Barrios), a qué carga.Obra corresponde — sin repetir el matching por
    capa (ver gdu/management/commands/vincular_obras_contrataciones.py). Una misma
    contratación puede estar vinculada a varias obras (ej. un proyecto grande dividido
    en "Grupo 1"/"Grupo 2" como obras separadas en carga que comparten expediente), así
    que la clave mapea a una lista, no a una sola obra.
    """
    resultado = defaultdict(list)
    for obra_id, obra_nombre, expediente in ObraContratacion.objects.select_related(
        "obra", "contratacion"
    ).values_list("obra_id", "obra__obra_nombre", "contratacion__expediente"):
        clave = normalizar_expediente(expediente)
        if clave is not None:
            resultado[clave].append({"id": obra_id, "nombre": obra_nombre})
    return resultado


def _bbox_polygon(request):
    """Bbox en la proyección del mapa (EPSG:3857), como la manda ol/loadingstrategy/bbox."""
    bbox = request.GET.get("bbox")
    if not bbox:
        return None
    try:
        minx, miny, maxx, maxy = (float(v) for v in bbox.split(","))
    except ValueError:
        return None
    poly = Polygon.from_bbox((minx, miny, maxx, maxy))
    poly.srid = MAP_SRID
    return poly


def _feature_collection(queryset, propiedades):
    features = []
    for obj in queryset:
        geom = obj.geom_4326
        if geom is None:
            continue
        features.append({
            "type": "Feature",
            "geometry": json.loads(geom.geojson),
            "properties": propiedades(obj),
        })
    return {"type": "FeatureCollection", "features": features}


def _geojson_capa(request, model, propiedades, filtros=None):
    """Respuesta GeoJSON genérica para una capa del visor: filtra por bbox (ol/loadingstrategy/bbox),
    opcionalmente por `filtros` (los criterios del modal de búsqueda avanzada) y arma las features
    con `propiedades`. Común a todas las capas de gdu/views/visor.py."""
    bbox = _bbox_polygon(request)
    if bbox is None:
        return HttpResponseBadRequest("falta el parámetro bbox")

    qs = (
        model.objects
        .annotate(geom_web=Transform("geom", MAP_SRID), geom_4326=Transform("geom", GEOJSON_SRID))
        .filter(geom_web__intersects=bbox)
    )
    if filtros:
        qs = qs.filter(**filtros)
    qs = qs[:MAX_FEATURES_POR_CAPA]
    return JsonResponse(_feature_collection(qs, propiedades))


def _filtros_texto(request, mapeo):
    """{parámetro de la query string: campo del modelo} -> kwargs de filter(), solo con los
    presentes y no vacíos. Usado para los criterios de texto del modal de búsqueda avanzada
    (Programa/Actuación/Estado de Gestión/Ley/Municipio)."""
    filtros = {}
    for parametro, campo in mapeo.items():
        valor = request.GET.get(parametro)
        if valor:
            filtros[campo] = valor
    return filtros


def _filtros_enteros(request, mapeo):
    """Igual que `_filtros_texto` pero para campos numéricos (Grupo/Plan de intervención);
    valores no convertibles a int se descartan en silencio."""
    filtros = {}
    for parametro, campo in mapeo.items():
        valor = request.GET.get(parametro)
        if valor:
            try:
                filtros[campo] = int(valor)
            except ValueError:
                pass
    return filtros


def _distintos_texto(*querysets_campo):
    """Valores distintos y no vacíos de uno o más (queryset, campo), combinados. Para poblar los
    combos del modal de búsqueda avanzada a partir de varias capas que comparten el mismo campo
    (ej. `programa`/`actuacion` en Barrios y Viviendas). El vacío se descarta en Python, no en SQL:
    algunos de estos campos (ej. `Expropiaciones.gestion`) son enums de Postgres donde comparar
    contra '' directamente en la query falla."""
    valores = set()
    for queryset, campo in querysets_campo:
        valores.update(
            queryset
            .exclude(**{f"{campo}__isnull": True})
            .values_list(campo, flat=True)
            .distinct()
        )
    valores.discard("")
    return sorted(valores)


def _distintos_enteros(queryset, campo):
    return sorted(set(
        queryset.exclude(**{f"{campo}__isnull": True}).values_list(campo, flat=True).distinct()
    ))


PERMISOS_CAPAS = [
    "gdu.ver_viviendas",
    "gdu.ver_barrios",
    "gdu.ver_expropiaciones",
    "gdu.ver_viviendas_dispersas",
    "gdu.ver_plano_mensura",
    "gdu.ver_catastro_urbano",
    "gdu.ver_escriturar",
]


@login_required
def mapa(request):
    # el visor combina varias capas; alcanza con poder ver alguna de ellas
    # (permission_required no soporta OR entre permisos, se chequea a mano)
    if not any(request.user.has_perm(p) for p in PERMISOS_CAPAS):
        raise PermissionDenied
    return render(request, "gdu/mapa.html")


FILTROS_TEXTO_PROGRAMA_ACTUACION = {"programa": "programa", "actuacion": "actuacion"}
FILTROS_ENTEROS_GRUPO_PLAN = {"grupo": "grupo", "plan": "plan"}


@permission_required("gdu.ver_viviendas", raise_exception=True)
def geojson_viviendas(request):
    obras_por_expediente = _obras_por_expediente()
    filtros = {
        **_filtros_texto(request, FILTROS_TEXTO_PROGRAMA_ACTUACION),
        **_filtros_enteros(request, FILTROS_ENTEROS_GRUPO_PLAN),
    }

    def propiedades(v):
        return {
            "id": v.id,
            "uf": v.uf,
            "obra": v.obra,
            "localidad": v.localidad,
            "adjudicacion": v.adjudicacion,
            "nro_adjudicatario": v.nro_adjudicatario,
            "estado_dominial": v.estado_dominial,
            "planos": v.planos,
            "obras": obras_por_expediente.get(normalizar_expediente(v.expediente), []),
        }

    return _geojson_capa(request, Viviendas, propiedades, filtros)


@login_required
def opciones_busqueda(request):
    """Valores para poblar los combos del modal de búsqueda avanzada (Programa, Actuación,
    Grupo, Plan, Estado de Gestión de Expropiación, Ley de Expropiación, Municipio) — mismos
    criterios que ofrece el buscador del sitio original de GDU."""
    return JsonResponse({
        "programas": _distintos_texto((Barrios.objects, "programa"), (Viviendas.objects, "programa")),
        "actuaciones": _distintos_texto((Barrios.objects, "actuacion"), (Viviendas.objects, "actuacion")),
        "grupos": _distintos_enteros(Viviendas.objects, "grupo"),
        "planes": _distintos_enteros(Viviendas.objects, "plan"),
        "estados_gestion": _distintos_texto((Expropiaciones.objects, "gestion")),
        "leyes": _distintos_texto((Expropiaciones.objects, "ley")),
        "municipios": _distintos_texto((Catastrourbano.objects, "municipio")),
    })


@login_required
def buscar_localidad(request):
    q = (request.GET.get("q") or "").strip()
    if len(q) < 2:
        return JsonResponse({"results": []})

    qs = (
        Localidad.objects
        .annotate(geom_4326=Transform("geom", GEOJSON_SRID))
        .filter(localidad__icontains=q)
        .order_by("localidad")[:15]
    )
    results = [
        {
            "id": loc.id,
            "text": f"{loc.localidad}, {loc.departamento}",
            "lon": loc.geom_4326.x,
            "lat": loc.geom_4326.y,
        }
        for loc in qs
    ]
    return JsonResponse({"results": results})


@login_required
def buscar_parcela(request):
    q = (request.GET.get("q") or "").strip()
    if len(q) < 2:
        return JsonResponse({"results": []})

    qs = (
        Parcela.objects
        .annotate(geom_web=Transform("geom", MAP_SRID))
        .filter(nomenclatura__icontains=q)
        .order_by("nomenclatura")[:15]
    )
    results = [
        {
            "id": p.id,
            "text": p.nomenclatura or f"{p.dpto}-{p.circ}-{p.secc}-{p.ch}-{p.qta}-{p.fracc}-{p.mz}-{p.parc}",
            "extent": list(p.geom_web.extent),
        }
        for p in qs
    ]
    return JsonResponse({"results": results})


@permission_required("gdu.ver_barrios", raise_exception=True)
def geojson_barrios(request):
    obras_por_expediente = _obras_por_expediente()
    filtros = _filtros_texto(request, FILTROS_TEXTO_PROGRAMA_ACTUACION)

    def propiedades(b):
        return {
            "id": b.id,
            "barrio": b.barrio,
            "localidad": b.localidad,
            "programa": b.programa,
            "obras": obras_por_expediente.get(normalizar_expediente(b.expediente), []),
        }

    return _geojson_capa(request, Barrios, propiedades, filtros)


@permission_required("gdu.ver_expropiaciones", raise_exception=True)
def geojson_expropiaciones(request):
    filtros = _filtros_texto(request, {"ley": "ley", "estado_gestion": "gestion"})

    def propiedades(e):
        return {
            "id": e.id,
            "ley": e.ley,
            "localidad": e.localidad,
            "nomenclatura": f"{e.dpto}-{e.circ}-{e.secc}-{e.ch}-{e.qta}-{e.fracc}-{e.mz}-{e.parc}",
            "objeto": e.objeto,
            "propietario_expropiado": e.propietario_expropiado,
            "estado": e.estado,
        }

    return _geojson_capa(request, Expropiaciones, propiedades, filtros)


@permission_required("gdu.ver_viviendas_dispersas", raise_exception=True)
def geojson_viviendas_dispersas(request):
    obras_por_expediente = _obras_por_expediente()
    filtros = {
        **_filtros_texto(request, FILTROS_TEXTO_PROGRAMA_ACTUACION),
        **_filtros_enteros(request, FILTROS_ENTEROS_GRUPO_PLAN),
    }

    def propiedades(v):
        return {
            "id": v.id,
            "obra": v.obra,
            "localidad": v.localidad,
            "adjudicacion": v.adjudicacion,
            "planos": v.planos,
            "obras": obras_por_expediente.get(normalizar_expediente(v.expediente), []),
        }

    return _geojson_capa(request, ViviendaDispersa, propiedades, filtros)


@permission_required("gdu.ver_plano_mensura", raise_exception=True)
def geojson_planos_mensura(request):
    def propiedades(p):
        return {
            "id": p.id,
            "plano": p.pm_antecedente or f"{p.depto}-{p.nro}-{p.ano}",
            "en_gdu": p.en_gdu,
            "sup_parcelas": p.sup_parcelas,
            "sup_calles": p.sup_calles,
            "sup_reserva": p.sup_reserva,
        }

    return _geojson_capa(request, PlanoMensura, propiedades)


@permission_required("gdu.ver_catastro_urbano", raise_exception=True)
def geojson_catastro_urbano(request):
    filtros = _filtros_texto(request, {"municipio": "municipio"})

    def propiedades(c):
        return {
            "id": c.id,
            "nomenclatura": c.id_nomencl,
            "plano_aprobado": c.plano_apro,
            "matricula": c.matric,
            "municipio": c.municipio,
            "anio": c.anio,
        }

    return _geojson_capa(request, Catastrourbano, propiedades, filtros)


@permission_required("gdu.ver_escriturar", raise_exception=True)
def geojson_para_escriturar(request):
    obras_por_expediente = _obras_por_expediente()
    filtros = {
        **_filtros_texto(request, FILTROS_TEXTO_PROGRAMA_ACTUACION),
        **_filtros_enteros(request, FILTROS_ENTEROS_GRUPO_PLAN),
    }

    def propiedades(v):
        return {
            "id": v.id,
            "uf": v.uf,
            "obra": v.obra,
            "localidad": v.localidad,
            "adjudicacion": v.adjudicacion,
            "nro_adjudicatario": v.nro_adjudicatario,
            "estado_dominial": v.estado_dominial,
            "planos": v.planos,
            "obras": obras_por_expediente.get(normalizar_expediente(v.expediente), []),
        }

    return _geojson_capa(request, ViviendasParaEscriturar, propiedades, filtros)
