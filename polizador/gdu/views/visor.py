from collections import defaultdict

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.gis.db.models.functions import AsGeoJSON, Transform
from django.contrib.gis.geos import Polygon
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
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
# Tope de features por pedido de cada capa. Con el GeoJSON sin properties (solo id + geometría):
# una vista full HD a zoom 15 en lo más denso de Resistencia tiene ~11k viviendas y entra entera;
# ~330 KB comprimido, y OpenLayers redibuja 12k polígonos en ~30 ms (con 30k ya baja a ~10 fps).
MAX_FEATURES_POR_CAPA = 12000
# decimales de las coordenadas (grados WGS84) en el GeoJSON del visor: 6 ≈ 10 cm, de sobra para
# dibujar. Con los 15 que salían por default el payload pesaba casi el doble ya comprimido.
GEOJSON_PRECISION = 6


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


def _geojson_capa(request, model, filtros=None):
    """Respuesta GeoJSON genérica para una capa del visor: filtra por bbox (ol/loadingstrategy/bbox)
    y opcionalmente por `filtros` (los criterios del modal de búsqueda avanzada). Común a todas las
    capas de gdu/views/visor.py.

    Cada feature trae solo id + geometría, sin properties: los datos para el panel de selección se
    piden aparte, al seleccionar (`detalle_capa`). Así el pedido pesa la mitad y la consulta no
    calcula las columnas de la vista que no se usan para dibujar."""
    bbox = _bbox_polygon(request)
    if bbox is None:
        return HttpResponseBadRequest("falta el parámetro bbox")

    # Filtrar sobre `geom` tal cual (no sobre Transform("geom", 3857)): Django reproyecta el bbox
    # al SRID de la columna y así Postgres puede usar el índice GiST. Con el Transform del lado de
    # la columna el índice no aplica, se evalúa fila por fila y el costo estimado dispara el JIT.
    # El GeoJSON de la geometría lo arma PostGIS (ST_AsGeoJSON), más rápido que pasar por GEOS.
    qs = model.objects.filter(geom__intersects=bbox)
    if filtros:
        qs = qs.filter(**filtros)
    qs = qs.annotate(
        geojson=AsGeoJSON(Transform("geom", GEOJSON_SRID), precision=GEOJSON_PRECISION),
    ).values_list("pk", "geojson")
    # se pide una de más para saber si el bbox quedó recortado; `truncado` (miembro extra del
    # FeatureCollection) le avisa al visor que tiene que volver a pedir el área al acercarse
    filas = list(qs[:MAX_FEATURES_POR_CAPA + 1])
    truncado = len(filas) > MAX_FEATURES_POR_CAPA
    # La geometría ya viene como texto JSON de PostGIS: se arma la respuesta pegando strings en vez
    # de parsearla y volver a serializarla (con miles de features, esa ida y vuelta es lo más caro).
    # El id va a nivel de feature: ol.source.Vector lo usa para no volver a agregar las features
    # que ya tiene cuando la estrategia bbox repide un área solapada.
    features = ",".join(
        '{"type":"Feature","id":%d,"properties":{},"geometry":%s}' % (pk, geojson)
        for pk, geojson in filas[:MAX_FEATURES_POR_CAPA]
        if geojson is not None
    )
    cuerpo = '{"type":"FeatureCollection","truncado":%s,"features":[%s]}' % (
        "true" if truncado else "false", features,
    )
    return HttpResponse(cuerpo, content_type="application/json")


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
    return render(request, "gdu/mapa.html", {
        "carto_api_key": settings.GDU_CARTO_API_KEY,
        "google_maps_api_key": settings.GDU_GOOGLE_MAPS_API_KEY,
        "max_ids_detalle": MAX_IDS_DETALLE,
    })


FILTROS_TEXTO_PROGRAMA_ACTUACION = {"programa": "programa", "actuacion": "actuacion"}
FILTROS_ENTEROS_GRUPO_PLAN = {"grupo": "grupo", "plan": "plan"}


@permission_required("gdu.ver_viviendas", raise_exception=True)
def geojson_viviendas(request):
    filtros = {
        **_filtros_texto(request, FILTROS_TEXTO_PROGRAMA_ACTUACION),
        **_filtros_enteros(request, FILTROS_ENTEROS_GRUPO_PLAN),
    }
    return _geojson_capa(request, Viviendas, filtros)


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
    filtros = _filtros_texto(request, FILTROS_TEXTO_PROGRAMA_ACTUACION)
    return _geojson_capa(request, Barrios, filtros)


@permission_required("gdu.ver_expropiaciones", raise_exception=True)
def geojson_expropiaciones(request):
    filtros = _filtros_texto(request, {"ley": "ley", "estado_gestion": "gestion"})
    return _geojson_capa(request, Expropiaciones, filtros)


@permission_required("gdu.ver_viviendas_dispersas", raise_exception=True)
def geojson_viviendas_dispersas(request):
    filtros = {
        **_filtros_texto(request, FILTROS_TEXTO_PROGRAMA_ACTUACION),
        **_filtros_enteros(request, FILTROS_ENTEROS_GRUPO_PLAN),
    }
    return _geojson_capa(request, ViviendaDispersa, filtros)


@permission_required("gdu.ver_plano_mensura", raise_exception=True)
def geojson_planos_mensura(request):
    return _geojson_capa(request, PlanoMensura)


@permission_required("gdu.ver_catastro_urbano", raise_exception=True)
def geojson_catastro_urbano(request):
    filtros = _filtros_texto(request, {"municipio": "municipio"})
    return _geojson_capa(request, Catastrourbano, filtros)


@permission_required("gdu.ver_escriturar", raise_exception=True)
def geojson_para_escriturar(request):
    filtros = {
        **_filtros_texto(request, FILTROS_TEXTO_PROGRAMA_ACTUACION),
        **_filtros_enteros(request, FILTROS_ENTEROS_GRUPO_PLAN),
    }
    return _geojson_capa(request, ViviendasParaEscriturar, filtros)


# --- Detalle de los elementos seleccionados en el visor ---
# Las propiedades que muestra el panel de selección, por capa. Antes viajaban en cada feature del
# GeoJSON; ahora el visor las pide recién al seleccionar (`detalle_capa`). `obras` recibe el
# resultado de _obras_por_expediente() (o None en las capas que no lo usan).

def _propiedades_vivienda(v, obras):
    return {
        "id": v.id,
        "uf": v.uf,
        "obra": v.obra,
        "localidad": v.localidad,
        "adjudicacion": v.adjudicacion,
        "nro_adjudicatario": v.nro_adjudicatario,
        "estado_dominial": v.estado_dominial,
        "planos": v.planos,
        "obras": obras.get(normalizar_expediente(v.expediente), []),
    }


def _propiedades_barrio(b, obras):
    return {
        "id": b.id,
        "barrio": b.barrio,
        "localidad": b.localidad,
        "programa": b.programa,
        "obras": obras.get(normalizar_expediente(b.expediente), []),
    }


def _propiedades_expropiacion(e, obras):
    return {
        "id": e.id,
        "ley": e.ley,
        "localidad": e.localidad,
        "nomenclatura": f"{e.dpto}-{e.circ}-{e.secc}-{e.ch}-{e.qta}-{e.fracc}-{e.mz}-{e.parc}",
        "objeto": e.objeto,
        "propietario_expropiado": e.propietario_expropiado,
        "estado": e.estado,
    }


def _propiedades_vivienda_dispersa(v, obras):
    return {
        "id": v.id,
        "obra": v.obra,
        "localidad": v.localidad,
        "adjudicacion": v.adjudicacion,
        "planos": v.planos,
        "obras": obras.get(normalizar_expediente(v.expediente), []),
    }


def _propiedades_plano_mensura(p, obras):
    return {
        "id": p.id,
        "plano": p.pm_antecedente or f"{p.depto}-{p.nro}-{p.ano}",
        "en_gdu": p.en_gdu,
        "sup_parcelas": p.sup_parcelas,
        "sup_calles": p.sup_calles,
        "sup_reserva": p.sup_reserva,
    }


def _propiedades_catastro_urbano(c, obras):
    return {
        "id": c.id,
        "nomenclatura": c.id_nomencl,
        "plano_aprobado": c.plano_apro,
        "matricula": c.matric,
        "municipio": c.municipio,
        "anio": c.anio,
    }


# slug de capa (los mismos que gdu:ficha) -> (modelo, permiso, propiedades, usa obras vinculadas)
CAPAS_DETALLE = {
    "viviendas": (Viviendas, "gdu.ver_viviendas", _propiedades_vivienda, True),
    "barrios": (Barrios, "gdu.ver_barrios", _propiedades_barrio, True),
    "expropiaciones": (Expropiaciones, "gdu.ver_expropiaciones", _propiedades_expropiacion, False),
    "viviendas-dispersas": (ViviendaDispersa, "gdu.ver_viviendas_dispersas", _propiedades_vivienda_dispersa, True),
    "planos-mensura": (PlanoMensura, "gdu.ver_plano_mensura", _propiedades_plano_mensura, False),
    "catastro-urbano": (Catastrourbano, "gdu.ver_catastro_urbano", _propiedades_catastro_urbano, False),
    "para-escriturar": (ViviendasParaEscriturar, "gdu.ver_escriturar", _propiedades_vivienda, True),
}

# tope de ids por pedido de detalle; el visor parte selecciones más grandes en varios pedidos
MAX_IDS_DETALLE = 500


@login_required
def detalle_capa(request, capa):
    """{id: propiedades} de los elementos `ids` (separados por coma) de una capa del visor, para el
    panel de selección."""
    if capa not in CAPAS_DETALLE:
        raise Http404
    model, permiso, propiedades, usa_obras = CAPAS_DETALLE[capa]
    if not request.user.has_perm(permiso):
        raise PermissionDenied
    try:
        ids = [int(v) for v in request.GET.get("ids", "").split(",") if v]
    except ValueError:
        return HttpResponseBadRequest("ids inválidos")
    if not ids or len(ids) > MAX_IDS_DETALLE:
        return HttpResponseBadRequest(f"entre 1 y {MAX_IDS_DETALLE} ids")

    obras = _obras_por_expediente() if usa_obras else None
    return JsonResponse({
        obj.pk: propiedades(obj, obras)
        for obj in model.objects.filter(pk__in=ids).defer("geom")
    })
