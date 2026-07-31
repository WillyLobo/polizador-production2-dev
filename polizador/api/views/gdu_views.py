# gdu app API views: datatable listings for the "catastro" core models.
import json

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from ninja import Router
from ninja.decorators import decorate_view

from api.permissions import require_model_perm
from api.views.generics import parse_order_by, register_simple_datatable
from carga.models import Obra
from gdu.models import (
    AdjudicacionBeneficiario,
    Adjudicatario3450,
    Actuacion,
    Barrio,
    Contratacion,
    DestinoParcela,
    EstadoGestionExpropiacion,
    Expropiacion,
    Intervencion,
    Localidad,
    Parcela,
    PlanoMensura,
    Programa,
    ResolucionCostos,
    TipoContratacion,
    TipoEstado,
    TipoIntervencion,
    TipoUf,
    Uf,
)

router = Router(tags=["gdu"])


# --- Actuacion ---
def _actuacion_row(a: Actuacion, user) -> dict:
    return {
        "id": a.id,
        "nombre": a.nombre,
        "ano": a.ano,
        "instrumento": a.instrumento,
        "programa": a.id_programa.nombre if a.id_programa else "",
    }


register_simple_datatable(
    router, Actuacion, "gdu-actuaciones",
    queryset=Actuacion.objects.select_related("id_programa"),
    order_fields={
        "id": "id", "nombre": "nombre", "ano": "ano", "instrumento": "instrumento",
        "programa": "id_programa__nombre",
    },
    filter_fields={
        "nombre": "nombre__icontains", "instrumento": "instrumento__icontains",
        "programa": "id_programa__nombre__icontains",
    },
    search_lookups=["nombre__icontains", "instrumento__icontains", "id_programa__nombre__icontains"],
    row_builder=_actuacion_row,
    default_order="nombre",
)


# --- Contratacion ---
def _contratacion_row(c: Contratacion, user) -> dict:
    return {
        "id": c.id,
        "nombre": c.nombre,
        "expediente": c.expediente,
        "resolucion": c.resolucion,
        "ano": c.ano,
        "tipo": c.tipo.nombre if c.tipo else "",
        "actuacion": c.id_actuacion.nombre if c.id_actuacion else "",
    }


register_simple_datatable(
    router, Contratacion, "gdu-contrataciones",
    queryset=Contratacion.objects.select_related("id_actuacion", "tipo"),
    order_fields={
        "id": "id", "nombre": "nombre", "expediente": "expediente", "resolucion": "resolucion",
        "ano": "ano", "tipo": "tipo__nombre", "actuacion": "id_actuacion__nombre",
    },
    filter_fields={
        "nombre": "nombre__icontains", "expediente": "expediente__icontains",
        "resolucion": "resolucion__icontains", "tipo": "tipo__nombre__icontains",
        "actuacion": "id_actuacion__nombre__icontains",
    },
    search_lookups=["nombre__icontains", "expediente__icontains", "resolucion__icontains"],
    row_builder=_contratacion_row,
    default_order="nombre",
)


# --- Contratacion sin obra vinculada (gdu.ObraContratacion) ---
def _contratacion_sin_obra_row(c: Contratacion, user) -> dict:
    row = _contratacion_row(c, user)
    row["programa"] = c.id_actuacion.id_programa.nombre if c.id_actuacion and c.id_actuacion.id_programa else ""
    return row


register_simple_datatable(
    router, Contratacion, "gdu-contrataciones-sin-obra",
    queryset=Contratacion.objects.filter(obras_vinculadas__isnull=True).select_related(
        "id_actuacion__id_programa", "tipo",
    ),
    order_fields={
        "id": "id", "nombre": "nombre", "expediente": "expediente", "resolucion": "resolucion",
        "ano": "ano", "tipo": "tipo__nombre", "actuacion": "id_actuacion__nombre",
        "programa": "id_actuacion__id_programa__nombre",
    },
    filter_fields={
        "nombre": "nombre__icontains", "expediente": "expediente__icontains",
        "resolucion": "resolucion__icontains", "tipo": "tipo__nombre__icontains",
        "actuacion": "id_actuacion__nombre__icontains",
        "programa": "id_actuacion__id_programa_id",
    },
    search_lookups=["nombre__icontains", "expediente__icontains", "resolucion__icontains"],
    row_builder=_contratacion_sin_obra_row,
    default_order="nombre",
    with_detail=False,
)


@router.get("/datatables/gdu-contrataciones-sin-obra/filtro-programa/")
@decorate_view(require_model_perm(Contratacion))
def datatable_gdu_contrataciones_sin_obra_filtro_programa(request):
    choices = (
        Contratacion.objects.filter(obras_vinculadas__isnull=True)
        .exclude(id_actuacion__id_programa=None)
        .values_list("id_actuacion__id_programa_id", "id_actuacion__id_programa__nombre")
        .distinct()
        .order_by("id_actuacion__id_programa__nombre")
    )
    return {"choices": list(choices)}


@router.get("/datatables/gdu-contrataciones-sin-obra/{id}/detalle/")
@decorate_view(require_model_perm(Contratacion))
def datatable_gdu_contrataciones_sin_obra_detalle(request, id: int):
    """Fila expandida de gdu-contrataciones-sin-obra: en vez del dump genérico de
    render_datatable_row_details, muestra la tabla anidada de gdu-obras-para-vincular
    (gdu/_contratacion_sin_obra_detail.html) para elegir y vincular la obra ahí mismo."""
    contratacion = get_object_or_404(Contratacion, id=id)
    html = render_to_string(
        "gdu/_contratacion_sin_obra_detail.html", {"contratacion": contratacion}, request=request,
    )
    return {"html": html}


# --- Obra (carga) sin contratación vinculada, para elegir desde gdu-contrataciones-sin-obra ---
def _obra_para_vincular_row(o: Obra, user) -> dict:
    row = {
        "id": o.id,
        "nombre": o.obra_nombre,
        "expediente": o.obra_expediente,
        "empresa": o.obra_empresa.empresa_nombre if o.obra_empresa else "",
        "programa": o.obra_programa.programa_nombre if o.obra_programa else "",
        "acciones": "",
    }
    if user.has_perm("gdu.add_obracontratacion"):
        row["acciones"] = (
            f'<button type="button" class="btn btn-sm btn-outline-primary vincular-esta-obra-btn" '
            f'data-obra-id="{o.id}">Vincular esta obra</button>'
        )
    return row


register_simple_datatable(
    router, Obra, "gdu-obras-para-vincular",
    queryset=Obra.objects.filter(gdu_contratacion__isnull=True).select_related("obra_empresa", "obra_programa"),
    order_fields={
        "id": "id", "nombre": "obra_nombre", "expediente": "obra_expediente",
        "empresa": "obra_empresa__empresa_nombre", "programa": "obra_programa__programa_nombre",
    },
    filter_fields={
        "nombre": "obra_nombre__icontains", "expediente": "obra_expediente__icontains",
        "empresa": "obra_empresa__empresa_nombre__icontains", "programa": "obra_programa_id",
    },
    search_lookups=[
        "obra_nombre__icontains", "obra_expediente__icontains", "obra_empresa__empresa_nombre__icontains",
    ],
    row_builder=_obra_para_vincular_row,
    default_order="nombre",
    with_detail=False,
)


# --- Intervencion ---
def _intervencion_row(i: Intervencion, user) -> dict:
    return {
        "id": i.id,
        "nombre": i.nombre,
        "tipo": i.tipo.nombre if i.tipo else "",
        "localidad": i.id_localidad.localidad if i.id_localidad else "",
        "contratacion": i.id_contratacion.nombre if i.id_contratacion else "",
        "avance": i.avance,
        "estado": i.estado.nombre if i.estado else "",
    }


register_simple_datatable(
    router, Intervencion, "gdu-intervenciones",
    queryset=Intervencion.objects.select_related("id_localidad", "id_contratacion", "tipo", "estado"),
    order_fields={
        "id": "id", "nombre": "nombre", "tipo": "tipo__nombre",
        "localidad": "id_localidad__localidad", "contratacion": "id_contratacion__nombre",
        "avance": "avance", "estado": "estado__nombre",
    },
    filter_fields={
        "nombre": "nombre__icontains", "tipo": "tipo__nombre__icontains",
        "localidad": "id_localidad__localidad__icontains",
        "estado": "estado__nombre__icontains",
    },
    search_lookups=["nombre__icontains"],
    row_builder=_intervencion_row,
    default_order="nombre",
)


# --- Programa (gdu) ---
def _programa_row(p: Programa, user) -> dict:
    return {"id": p.id, "nombre": p.nombre, "origen": p.origen, "fiinancia": p.fiinancia}


register_simple_datatable(
    router, Programa, "gdu-programas",
    order_fields={"id": "id", "nombre": "nombre", "origen": "origen"},
    filter_fields={"nombre": "nombre__icontains", "origen": "origen__icontains"},
    search_lookups=["nombre__icontains", "origen__icontains"],
    row_builder=_programa_row,
    default_order="nombre",
)


# --- Barrio ---
def _barrio_row(b: Barrio, user) -> dict:
    return {
        "id": b.id,
        "nombre": b.nombre,
        "intervencion": b.id_intervencion.nombre if b.id_intervencion else "",
    }


register_simple_datatable(
    router, Barrio, "gdu-barrios",
    queryset=Barrio.objects.select_related("id_intervencion"),
    order_fields={"id": "id", "nombre": "nombre", "intervencion": "id_intervencion__nombre"},
    filter_fields={
        "nombre": "nombre__icontains", "intervencion": "id_intervencion__nombre__icontains",
    },
    search_lookups=["nombre__icontains"],
    row_builder=_barrio_row,
    default_order="nombre",
)


# --- Parcela ---
def _parcela_row(p: Parcela, user) -> dict:
    return {
        "id": p.id,
        "nomenclatura": p.nomenclatura,
        "intervencion": p.id_intervencion.nombre if p.id_intervencion else "",
        "destino": p.destino.nombre if p.destino else "",
        "es_ph": p.es_ph,
    }


register_simple_datatable(
    router, Parcela, "gdu-parcelas",
    queryset=Parcela.objects.select_related("id_intervencion", "destino"),
    order_fields={
        "id": "id", "nomenclatura": "nomenclatura", "intervencion": "id_intervencion__nombre",
        "destino": "destino__nombre", "es_ph": "es_ph",
    },
    filter_fields={
        "nomenclatura": "nomenclatura__icontains",
        "intervencion": "id_intervencion__nombre__icontains",
        "destino": "destino__nombre__icontains",
    },
    search_lookups=["nomenclatura__icontains"],
    row_builder=_parcela_row,
    default_order="nomenclatura",
)


# --- Uf ---
def _uf_row(u: Uf, user) -> dict:
    return {
        "id": u.id,
        "uf": u.uf,
        "parcela": u.id_parcela.nomenclatura if u.id_parcela else "",
        "tipo": u.tipo.nombre if u.tipo else "",
        "nro_adjudicatario": u.nro_adjudicatario,
        "irregular": u.irregular,
        "fr_mat": u.fr_mat,
    }


register_simple_datatable(
    router, Uf, "gdu-ufs",
    queryset=Uf.objects.select_related("id_parcela", "tipo"),
    order_fields={
        "id": "id", "uf": "uf", "parcela": "id_parcela__nomenclatura", "tipo": "tipo__nombre",
        "nro_adjudicatario": "nro_adjudicatario", "irregular": "irregular", "fr_mat": "fr_mat",
    },
    filter_fields={
        "uf": "uf__icontains", "parcela": "id_parcela__nomenclatura__icontains",
        "tipo": "tipo__nombre__icontains", "fr_mat": "fr_mat__icontains",
    },
    search_lookups=["uf__icontains", "fr_mat__icontains"],
    row_builder=_uf_row,
    default_order="uf",
)


# --- Localidad (gdu) ---
def _localidad_row(l: Localidad, user) -> dict:
    return {
        "id": l.id,
        "localidad": l.localidad,
        "departamento": l.departamento,
        "provincia": l.provincia,
        "codloc": l.codloc,
    }


register_simple_datatable(
    router, Localidad, "gdu-localidades",
    order_fields={
        "id": "id", "localidad": "localidad", "departamento": "departamento",
        "provincia": "provincia", "codloc": "codloc",
    },
    filter_fields={
        "localidad": "localidad__icontains", "departamento": "departamento__icontains",
        "provincia": "provincia__icontains",
    },
    search_lookups=["localidad__icontains", "departamento__icontains"],
    row_builder=_localidad_row,
    default_order="localidad",
)


# --- Expropiacion ---
def _expropiacion_row(e: Expropiacion, user) -> dict:
    return {
        "id": e.id,
        "nro_ley": e.nro_ley,
        "ano_ley": e.ano_ley,
        "localidad": e.localidad.localidad if e.localidad else "",
        "asentamiento_nombre": e.asentamiento_nombre,
        "asentamiento": e.asentamiento,
    }


register_simple_datatable(
    router, Expropiacion, "gdu-expropiaciones",
    queryset=Expropiacion.objects.select_related("localidad"),
    order_fields={
        "id": "id", "nro_ley": "nro_ley", "ano_ley": "ano_ley",
        "localidad": "localidad__localidad", "asentamiento_nombre": "asentamiento_nombre",
        "asentamiento": "asentamiento",
    },
    filter_fields={
        "nro_ley": "nro_ley__icontains", "asentamiento_nombre": "asentamiento_nombre__icontains",
        "localidad": "localidad__localidad__icontains",
    },
    search_lookups=["asentamiento_nombre__icontains"],
    row_builder=_expropiacion_row,
    default_order="-nro_ley",
)


# --- PlanoMensura ---
def _plano_mensura_row(p: PlanoMensura, user) -> dict:
    return {
        "id": p.id,
        "pm_antecedente": p.pm_antecedente,
        "depto": p.depto,
        "nro": p.nro,
        "ano": p.ano,
        "en_gdu": p.en_gdu,
    }


register_simple_datatable(
    router, PlanoMensura, "gdu-planos-mensura",
    order_fields={
        "id": "id", "pm_antecedente": "pm_antecedente", "depto": "depto", "nro": "nro", "ano": "ano",
        "en_gdu": "en_gdu",
    },
    filter_fields={
        "pm_antecedente": "pm_antecedente__icontains", "depto": "depto__icontains",
    },
    search_lookups=["pm_antecedente__icontains"],
    row_builder=_plano_mensura_row,
    default_order="pm_antecedente",
)


# --- AdjudicacionBeneficiario ---
def _adjudicacion_beneficiario_row(a: AdjudicacionBeneficiario, user) -> dict:
    return {"id": a.id, "nro": a.nro, "ano": a.ano, "tipo": a.tipo}


register_simple_datatable(
    router, AdjudicacionBeneficiario, "gdu-adjudicaciones-beneficiario",
    order_fields={"id": "id", "nro": "nro", "ano": "ano", "tipo": "tipo"},
    filter_fields={"nro": "nro__icontains", "tipo": "tipo__icontains"},
    search_lookups=["nro__icontains"],
    row_builder=_adjudicacion_beneficiario_row,
    default_order="-ano",
)


# --- ResolucionCostos ---
def _resolucion_costos_row(r: ResolucionCostos, user) -> dict:
    return {"id": r.id, "nro_corto": r.nro_corto, "nro_largo": r.nro_largo, "ano": r.ano, "tipo": r.tipo}


register_simple_datatable(
    router, ResolucionCostos, "gdu-resoluciones-costos",
    order_fields={
        "id": "id", "nro_corto": "nro_corto", "nro_largo": "nro_largo", "ano": "ano", "tipo": "tipo",
    },
    filter_fields={"nro_corto": "nro_corto__icontains", "tipo": "tipo__icontains"},
    search_lookups=["nro_corto__icontains"],
    row_builder=_resolucion_costos_row,
    default_order="-ano",
)


# --- Tablas de tipo/lookup (id + nombre) ---
def _nombre_row(obj, user) -> dict:
    return {"id": obj.id, "nombre": obj.nombre}


for _model, _slug in (
    (TipoContratacion, "gdu-tipos-contratacion"),
    (TipoEstado, "gdu-tipos-estado"),
    (TipoIntervencion, "gdu-tipos-intervencion"),
    (TipoUf, "gdu-tipos-uf"),
    (DestinoParcela, "gdu-destinos-parcela"),
    (EstadoGestionExpropiacion, "gdu-estados-gestion-expropiacion"),
):
    register_simple_datatable(
        router, _model, _slug,
        order_fields={"id": "id", "nombre": "nombre"},
        filter_fields={"nombre": "nombre__icontains"},
        search_lookups=["nombre__icontains"],
        row_builder=_nombre_row,
        default_order="nombre",
    )


# --- Adjudicatario3450 ---
# Bespoke endpoint (no register_simple_datatable): su PK es `adjugisnroadju`, no
# `id`, y register_simple_datatable ordena siempre por "id" como desempate fijo.
_ADJ3450_ORDER_FIELDS = {
    "adjugisnroadju": "adjugisnroadju",
    "adjugisapeynom": "adjugisapeynom",
    "adjugisdireccion": "adjugisdireccion",
    "adjugisdni": "adjugisdni",
    "adjugissituacion": "adjugissituacion",
    "adjugisestadoreg": "adjugisestadoreg",
}

_ADJ3450_FILTER_FIELDS = {
    "adjugisapeynom": "adjugisapeynom__icontains",
    "adjugisdireccion": "adjugisdireccion__icontains",
    "adjugisdni": "adjugisdni__icontains",
    "adjugissituacion": "adjugissituacion__icontains",
    "adjugisestadoreg": "adjugisestadoreg__icontains",
}

_ADJ3450_SEARCH_LOOKUPS = [
    "adjugisapeynom__icontains", "adjugisdireccion__icontains", "adjugismatricula__icontains",
]


def _adjudicatario3450_row(a: Adjudicatario3450) -> dict:
    return {
        "id": a.adjugisnroadju,
        "adjugisnroadju": a.adjugisnroadju,
        "adjugisapeynom": a.adjugisapeynom,
        "adjugisdireccion": a.adjugisdireccion,
        "adjugisdni": a.adjugisdni,
        "adjugissituacion": a.adjugissituacion,
        "adjugisestadoreg": a.adjugisestadoreg,
    }


@router.get("/datatables/gdu-adjudicatarios-3450/", operation_id="datatable_gdu_adjudicatarios_3450_list")
@decorate_view(require_model_perm(Adjudicatario3450))
def datatable_adjudicatarios_3450(
    request,
    draw: int = 1,
    start: int = 0,
    length: int = 50,
    search: str = "",
    order_by: str = "adjugisapeynom",
    filters: str = "{}",
):
    qs = Adjudicatario3450.objects.all()
    records_total = qs.count()

    try:
        active_filters = json.loads(filters)
    except (TypeError, ValueError):
        active_filters = {}
    for key, value in active_filters.items():
        lookup = _ADJ3450_FILTER_FIELDS.get(key)
        if lookup and value not in (None, ""):
            qs = qs.filter(**{lookup: value})

    if search:
        search_q = Q()
        for lookup in _ADJ3450_SEARCH_LOOKUPS:
            search_q |= Q(**{lookup: search})
        qs = qs.filter(search_q).distinct()

    records_filtered = qs.count()
    qs = qs.order_by(
        *parse_order_by(order_by, _ADJ3450_ORDER_FIELDS, default_field="adjugisnroadju"),
        "adjugisnroadju",
    )
    page = qs[start:] if length == -1 else qs[start:start + length]

    return {
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": [_adjudicatario3450_row(o) for o in page],
    }
