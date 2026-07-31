import json
from collections import defaultdict

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.gis.db.models.functions import Transform
from django.contrib.gis.geos import Polygon
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from gdu.matching import normalizar_expediente
from gdu.models import Barrios, ObraContratacion, Viviendas

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
    obras_por_expediente = _obras_por_expediente()

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

    data = _feature_collection(qs, propiedades)
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
    obras_por_expediente = _obras_por_expediente()

    def propiedades(b):
        return {
            "id": b.id,
            "barrio": b.barrio,
            "localidad": b.localidad,
            "programa": b.programa,
            "obras": obras_por_expediente.get(normalizar_expediente(b.expediente), []),
        }

    data = _feature_collection(qs, propiedades)
    return JsonResponse(data)
