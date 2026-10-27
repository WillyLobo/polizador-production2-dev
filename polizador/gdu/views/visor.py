from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.gis.db.models.functions import AsGeoJSON, Transform
from django.contrib.gis.geos import Polygon
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from carga.models import Localidad
from gdu.capas import CAPAS, PERMISOS_CAPAS, filtros_de, obras_vinculadas
from gdu.models import Catastrourbano, Expropiacion, Intervencion, Parcela, Programa, Actuacion

MAP_SRID = 3857  # como la manda ol/loadingstrategy/bbox, para el filtro espacial
GEOJSON_SRID = 4326  # GeoJSON (RFC 7946) siempre es WGS84; ol.format.GeoJSON asume esto al reproyectar
# Tope de features por pedido de cada capa. Con el GeoJSON sin properties (solo id + geometría):
# una vista full HD a zoom 15 en lo más denso de Resistencia tiene ~11k viviendas y entra entera;
# ~330 KB comprimido, y OpenLayers redibuja 12k polígonos en ~30 ms (con 30k ya baja a ~10 fps).
MAX_FEATURES_POR_CAPA = 12000
# decimales de las coordenadas (grados WGS84) en el GeoJSON del visor: 6 ≈ 10 cm, de sobra para
# dibujar. Con los 15 que salían por default el payload pesaba casi el doble ya comprimido.
GEOJSON_PRECISION = 6


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


def _geojson_capa(request, queryset, filtros=None):
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
    qs = queryset.filter(geom__intersects=bbox)
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


def _distintos(queryset, campo):
    """Valores distintos y no vacíos de un campo, ordenados, para los combos de la búsqueda avanzada."""
    valores = set(queryset.exclude(**{f"{campo}__isnull": True}).values_list(campo, flat=True).distinct())
    valores.discard("")
    return sorted(valores)


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


def _vista_geojson(slug):
    capa = CAPAS[slug]

    @permission_required(capa.permiso, raise_exception=True)
    def vista(request):
        return _geojson_capa(request, capa.queryset(), filtros_de(request, capa))

    vista.__name__ = f"geojson_{slug.replace('-', '_')}"
    return vista


geojson_viviendas = _vista_geojson("viviendas")
geojson_barrios = _vista_geojson("barrios")
geojson_expropiaciones = _vista_geojson("expropiaciones")
geojson_viviendas_dispersas = _vista_geojson("viviendas-dispersas")
geojson_planos_mensura = _vista_geojson("planos-mensura")
geojson_catastro_urbano = _vista_geojson("catastro-urbano")
geojson_para_escriturar = _vista_geojson("para-escriturar")


@login_required
def opciones_busqueda(request):
    """Valores para poblar los combos del modal de búsqueda avanzada (Programa, Actuación,
    Grupo, Plan, Estado de Gestión de Expropiación, Ley de Expropiación, Municipio) — mismos
    criterios que ofrece el buscador del sitio original de GDU."""
    return JsonResponse({
        "programas": _distintos(Programa.objects, "nombre"),
        "actuaciones": _distintos(Actuacion.objects, "nombre"),
        "grupos": _distintos(Intervencion.objects, "grupo"),
        "planes": _distintos(Intervencion.objects, "plan"),
        "estados_gestion": [valor for valor, _ in Expropiacion.Gestion.choices],
        "leyes": _distintos(CAPAS["expropiaciones"].queryset(), "ley"),
        "municipios": _distintos(Catastrourbano.objects, "municipio"),
    })


@login_required
def buscar_localidad(request):
    q = (request.GET.get("q") or "").strip()
    if len(q) < 2:
        return JsonResponse({"results": []})

    qs = (
        Localidad.objects
        .select_related("localidad_departamento")
        .filter(localidad_nombre__icontains=q, localidad_centroide_lat__isnull=False)
        .order_by("localidad_nombre")[:15]
    )
    results = [
        {
            "id": loc.id,
            "text": f"{loc.localidad_nombre}, {loc.localidad_departamento.departamento_nombre}",
            "lon": float(loc.localidad_centroide_lon),
            "lat": float(loc.localidad_centroide_lat),
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
        {"id": p.id, "text": p.nomenclatura, "extent": list(p.geom_web.extent)}
        for p in qs
    ]
    return JsonResponse({"results": results})


# tope de ids por pedido de detalle; el visor parte selecciones más grandes en varios pedidos
MAX_IDS_DETALLE = 500


@login_required
def detalle_capa(request, capa):
    """{id: propiedades} de los elementos `ids` (separados por coma) de una capa del visor, para el
    panel de selección. Las properties no viajan en el GeoJSON: se piden recién al seleccionar."""
    if capa not in CAPAS:
        raise Http404
    config = CAPAS[capa]
    if not request.user.has_perm(config.permiso):
        raise PermissionDenied
    try:
        ids = [int(v) for v in request.GET.get("ids", "").split(",") if v]
    except ValueError:
        return HttpResponseBadRequest("ids inválidos")
    if not ids or len(ids) > MAX_IDS_DETALLE:
        return HttpResponseBadRequest(f"entre 1 y {MAX_IDS_DETALLE} ids")

    objetos = list(config.detalle_queryset().filter(pk__in=ids))
    obras = None
    if config.intervencion is not None:
        obras = obras_vinculadas(config.intervencion(o).contratacion_id for o in objetos)
    return JsonResponse({obj.pk: config.datos(obj, obras) for obj in objetos})
