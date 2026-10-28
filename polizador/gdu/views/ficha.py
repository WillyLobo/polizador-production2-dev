import json

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.gis.db.models.functions import Transform
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from gdu.auditoria import registrar_evento
from gdu.capas import CAPAS
from gdu.views import api3450
from gdu.views.visor import GEOJSON_SRID

# Cómo se dibuja cada capa del visor (gdu/templates/gdu/mapa.html), para mostrarla como
# contexto atenuado en la ficha: URL del GeoJSON y color/tipo/minZoom.
ESTILOS = {
    "viviendas": ("gdu:geojson_viviendas", {"color": "#dc3545", "tipo": "poligono", "minZoom": 13}),
    "barrios": ("gdu:geojson_barrios", {"color": "#0d6efd", "tipo": "poligono", "minZoom": 0}),
    "expropiaciones": ("gdu:geojson_expropiaciones", {"color": "#6f42c1", "tipo": "poligono", "minZoom": 0}),
    "viviendas-dispersas": ("gdu:geojson_viviendas_dispersas", {"color": "#20c997", "tipo": "punto", "minZoom": 12}),
    "planos-mensura": ("gdu:geojson_planos_mensura", {"color": "#6c757d", "tipo": "poligono", "minZoom": 13}),
    "catastro-urbano": ("gdu:geojson_catastro_urbano", {"color": "#495057", "tipo": "poligono", "minZoom": 14}),
    "para-escriturar": ("gdu:geojson_para_escriturar", {"color": "#198754", "tipo": "poligono", "minZoom": 13}),
}


def _formatear(valor):
    if valor is None or valor == "":
        return "-"
    if isinstance(valor, bool):
        return "Sí" if valor else "No"
    return str(valor)


def _filas(capa, datos):
    return [(etiqueta, _formatear(datos[clave])) for etiqueta, clave, _ in capa.campos]


CAMPOS_3450 = [
    ("Adjudicatario", "AdjuGISapeynom"),
    ("DNI", "AdjuGISdni"),
    ("Dirección", "AdjuGISdireccion"),
    ("Escriturado", "AdjuGISEscritura"),
    ("Matrícula", "AdjuGISmatricula"),
    ("Situación", "AdjuGISsituacion"),
    ("Motivo", "AdjuGISmotivo"),
]


def _datos_3450(datos):
    """
    Datos del Sistema 3450 para el Nº de adjudicatario del objeto, como en "Buscar 3450" del visor.
    None si la capa no tiene Nº de adjudicatario o está vacío; {"error": ...} si la API falla o no
    tiene datos (la API devuelve un registro vacío para números desconocidos).
    """
    nro = datos.get("nro_adjudicatario")
    if not nro:
        return None
    try:
        datos = api3450.consultar(nro).get("SDTDatosAdjuGIS") or {}
    except (requests.RequestException, ValueError):
        return {"error": "No se pudo consultar el Sistema 3450."}
    if not datos.get("AdjuGISapeynom"):
        return {"error": "Sin datos en el Sistema 3450."}
    return {"filas": [(etiqueta, _formatear(datos.get(clave))) for etiqueta, clave in CAMPOS_3450]}


@login_required
def ficha(request, capa, objeto_id):
    """
    Ficha imprimible (hoja A4 apaisada) de un elemento del visor: mapa con el elemento aislado,
    capa base elegible, capas de contexto atenuadas y una tarjeta con sus datos. Reemplaza al PDF
    genérico que armaba gdu/views/print_pdf.py; se imprime desde el navegador (window.print()),
    como detalle-fojademedicion.html. El centro/zoom/capa base iniciales llegan por query string
    desde el visor (x, y en EPSG:3857, z, base) y se leen en el template.
    """
    config = CAPAS.get(capa)
    if config is None:
        raise Http404("Capa desconocida")
    if not request.user.has_perm(config.permiso):
        raise PermissionDenied

    obj = get_object_or_404(
        config.relacionar(config.queryset()).annotate(geom_4326=Transform("geom", GEOJSON_SRID)),
        pk=objeto_id,
    )
    datos = config.datos(obj)
    registrar_evento(request, "printFeature", {"layer": capa, "id": obj.pk})

    capas_contexto = [
        {"capa": slug, "nombre": c.nombre, "url": reverse(ESTILOS[slug][0]), **ESTILOS[slug][1]}
        for slug, c in CAPAS.items()
        if request.user.has_perm(c.permiso)
    ]

    return render(request, "gdu/ficha.html", {
        "titulo": config.titulo,
        "objeto": obj,
        "filas": _filas(config, datos),
        "datos_3450": _datos_3450(datos),
        "fecha": timezone.localtime(),
        "config_mapa": {
            "geometria": json.loads(obj.geom_4326.geojson) if obj.geom_4326 else None,
            "estiloObjeto": ESTILOS[capa][1]["tipo"],
            "capasContexto": capas_contexto,
        },
        "carto_api_key": settings.GDU_CARTO_API_KEY,
        "google_maps_api_key": settings.GDU_GOOGLE_MAPS_API_KEY,
    })
