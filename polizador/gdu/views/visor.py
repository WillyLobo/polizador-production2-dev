import json

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.gis.db.models.functions import Transform
from django.contrib.gis.geos import Polygon
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from gdu.models import Barrios, Viviendas

MAP_SRID = 3857  # como la manda ol/loadingstrategy/bbox, para el filtro espacial
GEOJSON_SRID = 4326  # GeoJSON (RFC 7946) siempre es WGS84; ol.format.GeoJSON asume esto al reproyectar
MAX_FEATURES_POR_CAPA = 3000


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


@login_required
def mapa(request):
    # el visor combina ambas capas; alcanza con poder ver alguna de las dos
    # (permission_required no soporta OR entre permisos, se chequea a mano)
    if not (request.user.has_perm("gdu.ver_viviendas") or request.user.has_perm("gdu.ver_barrios")):
        raise PermissionDenied
    return render(request, "gdu/mapa.html")


@permission_required("gdu.ver_viviendas", raise_exception=True)
def geojson_viviendas(request):
    bbox = _bbox_polygon(request)
    if bbox is None:
        return HttpResponseBadRequest("falta el parámetro bbox")

    qs = (
        Viviendas.objects
        .annotate(geom_web=Transform("geom", MAP_SRID), geom_4326=Transform("geom", GEOJSON_SRID))
        .filter(geom_web__intersects=bbox)
        [:MAX_FEATURES_POR_CAPA]
    )
    data = _feature_collection(qs, lambda v: {
        "id": v.id,
        "uf": v.uf,
        "obra": v.obra,
        "localidad": v.localidad,
        "adjudicacion": v.adjudicacion,
        "nro_adjudicatario": v.nro_adjudicatario,
        "estado_dominial": v.estado_dominial,
        "planos": v.planos,
    })
    return JsonResponse(data)


@permission_required("gdu.ver_barrios", raise_exception=True)
def geojson_barrios(request):
    bbox = _bbox_polygon(request)
    if bbox is None:
        return HttpResponseBadRequest("falta el parámetro bbox")

    qs = (
        Barrios.objects
        .annotate(geom_web=Transform("geom", MAP_SRID), geom_4326=Transform("geom", GEOJSON_SRID))
        .filter(geom_web__intersects=bbox)
        [:MAX_FEATURES_POR_CAPA]
    )
    data = _feature_collection(qs, lambda b: {
        "id": b.id,
        "barrio": b.barrio,
        "localidad": b.localidad,
        "programa": b.programa,
    })
    return JsonResponse(data)
