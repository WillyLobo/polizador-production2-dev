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

from gdu.matching import normalizar_expediente
from gdu.models import (
    Barrios,
    Catastrourbano,
    Expropiaciones,
    PlanoMensura,
    ViviendaDispersa,
    Viviendas,
    ViviendasParaEscriturar,
)
from gdu.views import api3450
from gdu.views.visor import GEOJSON_SRID, _obras_por_expediente

OBRAS_VINCULADAS = "obras_vinculadas"  # marcador de campo: obras de carga resueltas por expediente


def _nomenclatura(o):
    return f"{o.dpto}-{o.circ}-{o.secc}-{o.ch}-{o.qta}-{o.fracc}-{o.mz}-{o.parc}"


CAMPOS_VIVIENDA = [
    ("UF", "uf"),
    ("Obra", "obra"),
    ("Localidad", "localidad"),
    ("Adjudicación", "adjudicacion"),
    ("Nº adjudicatario", "nro_adjudicatario"),
    ("Estado dominial", "estado_dominial"),
    ("Planos", "planos"),
    ("Obras vinculadas", OBRAS_VINCULADAS),
]

# Una entrada por capa del visor. Los campos de la ficha son los mismos que expone el GeoJSON
# de la capa (gdu/views/visor.py), menos el id, con etiqueta en castellano; `estilo` replica
# el color/tipo/minZoom de la capa en el visor (gdu/templates/gdu/mapa.html) para dibujarla
# como contexto atenuado.
CAPAS = {
    "viviendas": {
        "modelo": Viviendas,
        "permiso": "gdu.ver_viviendas",
        "titulo": "Vivienda",
        "nombre_capa": "Viviendas",
        "geojson": "gdu:geojson_viviendas",
        "estilo": {"color": "#dc3545", "tipo": "poligono", "minZoom": 13},
        "campos": CAMPOS_VIVIENDA,
    },
    "barrios": {
        "modelo": Barrios,
        "permiso": "gdu.ver_barrios",
        "titulo": "Barrio",
        "nombre_capa": "Barrios",
        "geojson": "gdu:geojson_barrios",
        "estilo": {"color": "#0d6efd", "tipo": "poligono", "minZoom": 0},
        "campos": [
            ("Barrio", "barrio"),
            ("Localidad", "localidad"),
            ("Programa", "programa"),
            ("Obras vinculadas", OBRAS_VINCULADAS),
        ],
    },
    "expropiaciones": {
        "modelo": Expropiaciones,
        "permiso": "gdu.ver_expropiaciones",
        "titulo": "Expropiación",
        "nombre_capa": "Expropiaciones",
        "geojson": "gdu:geojson_expropiaciones",
        "estilo": {"color": "#6f42c1", "tipo": "poligono", "minZoom": 0},
        "campos": [
            ("Ley", "ley"),
            ("Localidad", "localidad"),
            ("Nomenclatura", _nomenclatura),
            ("Objeto", "objeto"),
            ("Propietario expropiado", "propietario_expropiado"),
            ("Estado", "estado"),
        ],
    },
    "viviendas-dispersas": {
        "modelo": ViviendaDispersa,
        "permiso": "gdu.ver_viviendas_dispersas",
        "titulo": "Vivienda dispersa",
        "nombre_capa": "Viviendas Dispersas",
        "geojson": "gdu:geojson_viviendas_dispersas",
        "estilo": {"color": "#20c997", "tipo": "punto", "minZoom": 12},
        "campos": [
            ("Obra", "obra"),
            ("Localidad", "localidad"),
            ("Adjudicación", "adjudicacion"),
            ("Planos", "planos"),
            ("Obras vinculadas", OBRAS_VINCULADAS),
        ],
    },
    "planos-mensura": {
        "modelo": PlanoMensura,
        "permiso": "gdu.ver_plano_mensura",
        "titulo": "Plano de mensura",
        "nombre_capa": "Planos de Mensura",
        "geojson": "gdu:geojson_planos_mensura",
        "estilo": {"color": "#6c757d", "tipo": "poligono", "minZoom": 13},
        "campos": [
            ("Plano", lambda p: p.pm_antecedente or f"{p.depto}-{p.nro}-{p.ano}"),
            ("En GDU", "en_gdu"),
            ("Sup. parcelas", "sup_parcelas"),
            ("Sup. calles", "sup_calles"),
            ("Sup. reserva", "sup_reserva"),
        ],
    },
    "catastro-urbano": {
        "modelo": Catastrourbano,
        "permiso": "gdu.ver_catastro_urbano",
        "titulo": "Catastro urbano",
        "nombre_capa": "Catastro Urbano",
        "geojson": "gdu:geojson_catastro_urbano",
        "estilo": {"color": "#495057", "tipo": "poligono", "minZoom": 14},
        "campos": [
            ("Nomenclatura", "id_nomencl"),
            ("Plano aprobado", "plano_apro"),
            ("Matrícula", "matric"),
            ("Municipio", "municipio"),
            ("Año", "anio"),
        ],
    },
    "para-escriturar": {
        "modelo": ViviendasParaEscriturar,
        "permiso": "gdu.ver_escriturar",
        "titulo": "Vivienda para escriturar",
        "nombre_capa": "Para Escriturar",
        "geojson": "gdu:geojson_para_escriturar",
        "estilo": {"color": "#198754", "tipo": "poligono", "minZoom": 13},
        "campos": CAMPOS_VIVIENDA,
    },
}


def _formatear(valor):
    if valor is None or valor == "":
        return "-"
    if isinstance(valor, bool):
        return "Sí" if valor else "No"
    return str(valor)


def _filas(obj, campos):
    filas = []
    for etiqueta, campo in campos:
        if campo == OBRAS_VINCULADAS:
            obras = _obras_por_expediente().get(normalizar_expediente(obj.expediente), [])
            valor = ", ".join(o["nombre"] or f"Obra {o['id']}" for o in obras)
        elif callable(campo):
            valor = campo(obj)
        else:
            valor = getattr(obj, campo)
        filas.append((etiqueta, _formatear(valor)))
    return filas


CAMPOS_3450 = [
    ("Adjudicatario", "AdjuGISapeynom"),
    ("DNI", "AdjuGISdni"),
    ("Dirección", "AdjuGISdireccion"),
    ("Escriturado", "AdjuGISEscritura"),
    ("Matrícula", "AdjuGISmatricula"),
    ("Situación", "AdjuGISsituacion"),
    ("Motivo", "AdjuGISmotivo"),
]


def _datos_3450(obj):
    """
    Datos del Sistema 3450 para el Nº de adjudicatario del objeto, como en "Buscar 3450" del visor.
    None si la capa no tiene Nº de adjudicatario o está vacío; {"error": ...} si la API falla o no
    tiene datos (la API devuelve un registro vacío para números desconocidos).
    """
    nro = getattr(obj, "nro_adjudicatario", None)
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
    if not request.user.has_perm(config["permiso"]):
        raise PermissionDenied

    obj = get_object_or_404(
        config["modelo"].objects.annotate(geom_4326=Transform("geom", GEOJSON_SRID)),
        pk=objeto_id,
    )

    capas_contexto = [
        {
            "capa": slug,
            "nombre": c["nombre_capa"],
            "url": reverse(c["geojson"]),
            **c["estilo"],
        }
        for slug, c in CAPAS.items()
        if request.user.has_perm(c["permiso"])
    ]

    return render(request, "gdu/ficha.html", {
        "titulo": config["titulo"],
        "objeto": obj,
        "filas": _filas(obj, config["campos"]),
        "datos_3450": _datos_3450(obj),
        "fecha": timezone.localtime(),
        "config_mapa": {
            "geometria": json.loads(obj.geom_4326.geojson) if obj.geom_4326 else None,
            "estiloObjeto": config["estilo"]["tipo"],
            "capasContexto": capas_contexto,
        },
        "carto_api_key": settings.GDU_CARTO_API_KEY,
        "google_maps_api_key": settings.GDU_GOOGLE_MAPS_API_KEY,
    })
