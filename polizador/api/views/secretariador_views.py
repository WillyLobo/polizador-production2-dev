# secretariador app API views
import json
from typing import List

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from ninja import Router
from ninja.decorators import decorate_view
from ninja.pagination import paginate

from api.permissions import get_group_perms, require_model_perm
from api.views.generics import (
    PerPagePagination,
    clip_value_html,
    parse_order_by,
    register_simple_datatable,
)
from polizador.vars import detallelinkimg, editlinkimg, eliminarlinkimg, generarlinkimg, pdflinkimg
from api.schemas.secretariador_schemas import (
    MemorandumOut, MemorandumCreate, MemorandumUpdate,
    ResolucionOut, ResolucionCreate, ResolucionUpdate,
    DecretoOut, DecretoCreate,
    MontoViaticoOut, MontoViaticoCreate,
    ComisionadoOut, ComisionadoCreate,
    OrganigramaOut, OrganigramaCreate,
    VehiculoOut, VehiculoCreate,
    SolicitudOut, SolicitudCreate,
    ComisionadoSolicitudOut, ComisionadoSolicitudCreate,
    IncorporacionOut, IncorporacionCreate,
)
from secretariador.models import (
    ComisionadoSolicitud,
    Incorporacion,
    InstrumentosLegalesDecretos,
    InstrumentosLegalesMemorandum,
    InstrumentosLegalesResoluciones,
    MontoViaticoDiario,
    Organigrama,
    Solicitud,
    Vehiculo,
)
from personalizador.models import Agente

router = Router(tags=["secretariador"])


# --- Memorandum ---
@router.get("/memorandums/", response=List[MemorandumOut])
@decorate_view(require_model_perm(InstrumentosLegalesMemorandum))
@paginate(PerPagePagination)
def list_memorandums(request, ano: str = ""):
    qs = InstrumentosLegalesMemorandum.objects.all().order_by("-id")
    if ano:
        qs = qs.filter(instrumentolegalmemorandum_ano=ano)
    return qs


@router.get("/memorandum/{id}/", response=MemorandumOut)
@decorate_view(require_model_perm(InstrumentosLegalesMemorandum))
def retrieve_memorandum(request, id: int):
    return get_object_or_404(InstrumentosLegalesMemorandum, id=id)


@router.post("/memorandums/", response=MemorandumOut)
@decorate_view(require_model_perm(InstrumentosLegalesMemorandum))
def create_memorandum(request, payload: MemorandumCreate):
    m = InstrumentosLegalesMemorandum.objects.create(**payload.model_dump())
    m.refresh_from_db()
    return m


@router.put("/memorandum/{id}/", response=MemorandumOut)
@decorate_view(require_model_perm(InstrumentosLegalesMemorandum))
def update_memorandum(request, id: int, payload: MemorandumUpdate):
    m = get_object_or_404(InstrumentosLegalesMemorandum, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(m, field, value)
    m.save()
    return m


@router.delete("/memorandum/{id}/")
@decorate_view(require_model_perm(InstrumentosLegalesMemorandum))
def delete_memorandum(request, id: int):
    deleted, _ = InstrumentosLegalesMemorandum.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Resoluciones ---
@router.get("/resoluciones/", response=List[ResolucionOut])
@decorate_view(require_model_perm(InstrumentosLegalesResoluciones))
@paginate(PerPagePagination)
def list_resoluciones(request, ano: str = ""):
    qs = InstrumentosLegalesResoluciones.objects.all().order_by("-id")
    if ano:
        qs = qs.filter(instrumentolegalresoluciones_ano=ano)
    return qs


@router.get("/resolucion/{id}/", response=ResolucionOut)
@decorate_view(require_model_perm(InstrumentosLegalesResoluciones))
def retrieve_resolucion(request, id: int):
    return get_object_or_404(InstrumentosLegalesResoluciones, id=id)


@router.post("/resoluciones/", response=ResolucionOut)
@decorate_view(require_model_perm(InstrumentosLegalesResoluciones))
def create_resolucion(request, payload: ResolucionCreate):
    r = InstrumentosLegalesResoluciones.objects.create(**payload.model_dump())
    r.refresh_from_db()
    return r


@router.put("/resolucion/{id}/", response=ResolucionOut)
@decorate_view(require_model_perm(InstrumentosLegalesResoluciones))
def update_resolucion(request, id: int, payload: ResolucionUpdate):
    r = get_object_or_404(InstrumentosLegalesResoluciones, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(r, field, value)
    r.save()
    return r


@router.delete("/resolucion/{id}/")
@decorate_view(require_model_perm(InstrumentosLegalesResoluciones))
def delete_resolucion(request, id: int):
    deleted, _ = InstrumentosLegalesResoluciones.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Resoluciones Directorio ---
@router.get("/resoluciones-directorio/", response=List[ResolucionOut])
@decorate_view(require_model_perm(InstrumentosLegalesResoluciones))
@paginate(PerPagePagination)
def list_resoluciones_directorio(request, ano: str = ""):
    qs = InstrumentosLegalesResoluciones.objects.filter(instrumentolegalresoluciones_tipo="D").order_by("-id")
    if ano:
        qs = qs.filter(instrumentolegalresoluciones_ano=ano)
    return qs


@router.post("/resoluciones-directorio/", response=ResolucionOut)
@decorate_view(require_model_perm(InstrumentosLegalesResoluciones))
def create_resolucion_directorio(request, payload: ResolucionCreate):
    data = payload.model_dump()
    data["instrumentolegalresoluciones_tipo"] = "D"
    r = InstrumentosLegalesResoluciones.objects.create(**data)
    r.refresh_from_db()
    return r


@router.delete("/resolucion-directorio/{id}/")
@decorate_view(require_model_perm(InstrumentosLegalesResoluciones))
def delete_resolucion_directorio(request, id: int):
    deleted, _ = InstrumentosLegalesResoluciones.objects.filter(id=id, instrumentolegalresoluciones_tipo="D").delete()
    return {"deleted": bool(deleted)}


# --- Decretos ---
@router.get("/decretos/", response=List[DecretoOut])
@decorate_view(require_model_perm(InstrumentosLegalesDecretos))
@paginate(PerPagePagination)
def list_decretos(request, ano: str = ""):
    qs = InstrumentosLegalesDecretos.objects.all().order_by("-id")
    if ano:
        qs = qs.filter(instrumentolegaldecretos_ano=ano)
    return qs


@router.get("/decreto/{id}/", response=DecretoOut)
@decorate_view(require_model_perm(InstrumentosLegalesDecretos))
def retrieve_decreto(request, id: int):
    return get_object_or_404(InstrumentosLegalesDecretos, id=id)


@router.post("/decretos/", response=DecretoOut)
@decorate_view(require_model_perm(InstrumentosLegalesDecretos))
def create_decreto(request, payload: DecretoCreate):
    d = InstrumentosLegalesDecretos.objects.create(**payload.model_dump())
    d.refresh_from_db()
    return d


@router.delete("/decreto/{id}/")
@decorate_view(require_model_perm(InstrumentosLegalesDecretos))
def delete_decreto(request, id: int):
    deleted, _ = InstrumentosLegalesDecretos.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Memorandum datatable ---
def _memorandum_datatable_row(m: InstrumentosLegalesMemorandum, user) -> dict:
    id_ = str(m.id)
    editarlink = f"<a href='/viaticos/crearmemorandum/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href='/viaticos/crearmemorandum/ver/{id_}'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/viaticos/eliminar/memorandum/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("secretariador.delete_instrumentoslegalesmemorandum"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("secretariador.change_instrumentoslegalesmemorandum"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {
        "id": m.id,
        "instrumentolegalmemorandum_tipo": m.get_instrumentolegalmemorandum_tipo_display(),
        "instrumentolegalmemorandum_numero": m.instrumentolegalmemorandum_numero,
        "instrumentolegalmemorandum_ano": m.instrumentolegalmemorandum_ano,
        "instrumentolegalmemorandum_fecha_aprobacion": m.instrumentolegalmemorandum_fecha_aprobacion.isoformat(),
        "instrumentolegalmemorandum_descripcion": m.instrumentolegalmemorandum_descripcion,
        "instrumentolegalmemorandum_document": clip_value_html(m.instrumentolegalmemorandum_document or "", 200),
        "acciones": acciones,
    }


register_simple_datatable(
    router, InstrumentosLegalesMemorandum, "memorandums",
    order_fields={
        "id": "id",
        "instrumentolegalmemorandum_tipo": "instrumentolegalmemorandum_tipo",
        "instrumentolegalmemorandum_numero": "instrumentolegalmemorandum_numero",
        "instrumentolegalmemorandum_ano": "instrumentolegalmemorandum_ano",
        "instrumentolegalmemorandum_fecha_aprobacion": "instrumentolegalmemorandum_fecha_aprobacion",
        "instrumentolegalmemorandum_descripcion": "instrumentolegalmemorandum_descripcion",
    },
    filter_fields={
        "instrumentolegalmemorandum_tipo": "instrumentolegalmemorandum_tipo__icontains",
        "instrumentolegalmemorandum_numero": "instrumentolegalmemorandum_numero__icontains",
        "instrumentolegalmemorandum_ano": "instrumentolegalmemorandum_ano__icontains",
        "instrumentolegalmemorandum_fecha_aprobacion": "instrumentolegalmemorandum_fecha_aprobacion",
        "instrumentolegalmemorandum_descripcion": "instrumentolegalmemorandum_descripcion__icontains",
        "instrumentolegalmemorandum_document": "instrumentolegalmemorandum_document__icontains",
    },
    search_lookups=[
        "instrumentolegalmemorandum_numero__icontains", "instrumentolegalmemorandum_ano__icontains",
        "instrumentolegalmemorandum_descripcion__icontains", "instrumentolegalmemorandum_document__icontains",
    ],
    row_builder=_memorandum_datatable_row,
    default_order="-instrumentolegalmemorandum_ano,-instrumentolegalmemorandum_numero",
)


# --- Decretos datatable ---
def _decreto_datatable_row(d: InstrumentosLegalesDecretos, user) -> dict:
    id_ = str(d.id)
    editarlink = f"<a href='{d.get_absolute_url()}'>{editlinkimg}</a>"
    detallelink = f"<a href='/viaticos/creardecreto/ver/{id_}'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/viaticos/eliminar/decreto/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("secretariador.delete_instrumentoslegalesdecretos"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("secretariador.change_instrumentoslegalesdecretos"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {
        "id": d.id,
        "instrumentolegaldecretos_tipo": d.get_instrumentolegaldecretos_tipo_display(),
        "instrumentolegaldecretos_numero": d.instrumentolegaldecretos_numero,
        "instrumentolegaldecretos_ano": d.instrumentolegaldecretos_ano,
        "instrumentolegaldecretos_fecha_aprobacion": d.instrumentolegaldecretos_fecha_aprobacion.isoformat(),
        "instrumentolegaldecretos_descripcion": d.instrumentolegaldecretos_descripcion,
        "acciones": acciones,
    }


register_simple_datatable(
    router, InstrumentosLegalesDecretos, "decretos",
    order_fields={
        "id": "id",
        "instrumentolegaldecretos_tipo": "instrumentolegaldecretos_tipo",
        "instrumentolegaldecretos_numero": "instrumentolegaldecretos_numero",
        "instrumentolegaldecretos_ano": "instrumentolegaldecretos_ano",
        "instrumentolegaldecretos_fecha_aprobacion": "instrumentolegaldecretos_fecha_aprobacion",
        "instrumentolegaldecretos_descripcion": "instrumentolegaldecretos_descripcion",
    },
    filter_fields={
        "instrumentolegaldecretos_tipo": "instrumentolegaldecretos_tipo__icontains",
        "instrumentolegaldecretos_numero": "instrumentolegaldecretos_numero__icontains",
        "instrumentolegaldecretos_ano": "instrumentolegaldecretos_ano__icontains",
        "instrumentolegaldecretos_fecha_aprobacion": "instrumentolegaldecretos_fecha_aprobacion",
        "instrumentolegaldecretos_descripcion": "instrumentolegaldecretos_descripcion__icontains",
    },
    search_lookups=[
        "instrumentolegaldecretos_numero__icontains", "instrumentolegaldecretos_ano__icontains",
        "instrumentolegaldecretos_descripcion__icontains",
    ],
    row_builder=_decreto_datatable_row,
    default_order="-instrumentolegaldecretos_ano,-instrumentolegaldecretos_numero",
)


# --- Resoluciones (Presidencia + Directorio mezcladas) datatable ---
def _resolucion_datatable_row(r: InstrumentosLegalesResoluciones, user) -> dict:
    id_ = str(r.id)
    if r.instrumentolegalresoluciones_tipo == "P":
        editarlink = f"<a href='/viaticos/crearresolucionpresidencia/{id_}'>{editlinkimg}</a>"
    else:
        editarlink = f"<a href='/viaticos/crearresoluciondirectorio/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href='/viaticos/crearresolucion/ver/{id_}'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/viaticos/eliminar/resolucionpresidencia/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("secretariador.delete_instrumentoslegalesresoluciones"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("secretariador.change_instrumentoslegalesresoluciones"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {
        "id": r.id,
        "instrumentolegalresoluciones_tipo": r.get_instrumentolegalresoluciones_tipo_display(),
        "instrumentolegalresoluciones_numero": r.instrumentolegalresoluciones_numero,
        "instrumentolegalresoluciones_ano": r.instrumentolegalresoluciones_ano,
        "instrumentolegalresoluciones_fecha_aprobacion": r.instrumentolegalresoluciones_fecha_aprobacion.isoformat(),
        "instrumentolegalresoluciones_descripcion": clip_value_html(r.instrumentolegalresoluciones_descripcion, 200),
        "instrumentolegalresoluciones_document": clip_value_html(r.instrumentolegalresoluciones_document or "", 200),
        "acciones": acciones,
    }


_RESOLUCION_ORDER_FIELDS = {
    "id": "id",
    "instrumentolegalresoluciones_tipo": "instrumentolegalresoluciones_tipo",
    "instrumentolegalresoluciones_numero": "instrumentolegalresoluciones_numero",
    "instrumentolegalresoluciones_ano": "instrumentolegalresoluciones_ano",
    "instrumentolegalresoluciones_fecha_aprobacion": "instrumentolegalresoluciones_fecha_aprobacion",
    "instrumentolegalresoluciones_descripcion": "instrumentolegalresoluciones_descripcion",
}

_RESOLUCION_FILTER_FIELDS = {
    "instrumentolegalresoluciones_tipo": "instrumentolegalresoluciones_tipo__icontains",
    "instrumentolegalresoluciones_numero": "instrumentolegalresoluciones_numero__icontains",
    "instrumentolegalresoluciones_ano": "instrumentolegalresoluciones_ano__icontains",
    "instrumentolegalresoluciones_fecha_aprobacion": "instrumentolegalresoluciones_fecha_aprobacion",
    "instrumentolegalresoluciones_descripcion": "instrumentolegalresoluciones_descripcion__icontains",
    "instrumentolegalresoluciones_document": "instrumentolegalresoluciones_document__icontains",
}

register_simple_datatable(
    router, InstrumentosLegalesResoluciones, "resoluciones",
    order_fields=_RESOLUCION_ORDER_FIELDS,
    filter_fields=_RESOLUCION_FILTER_FIELDS,
    search_lookups=[
        "instrumentolegalresoluciones_numero__icontains", "instrumentolegalresoluciones_ano__icontains",
        "instrumentolegalresoluciones_descripcion__icontains", "instrumentolegalresoluciones_document__icontains",
    ],
    row_builder=_resolucion_datatable_row,
    default_order="-instrumentolegalresoluciones_ano,-instrumentolegalresoluciones_numero",
)


# --- Resoluciones de Directorio (solo tipo="D", con columna "acta") datatable ---
def _resolucion_directorio_datatable_row(r: InstrumentosLegalesResoluciones, user) -> dict:
    id_ = str(r.id)
    editarlink = f"<a href='/viaticos/crearresoluciondirectorio/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href='/viaticos/crearresoluciondirectorio/ver/{id_}'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/viaticos/eliminar/resoluciondirectorio/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("secretariador.delete_instrumentoslegalesresoluciones"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("secretariador.change_instrumentoslegalesresoluciones"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {
        "id": r.id,
        "instrumentolegalresoluciones_tipo": r.get_instrumentolegalresoluciones_tipo_display(),
        "instrumentolegalresoluciones_numero": r.instrumentolegalresoluciones_numero,
        "instrumentolegalresoluciones_acta": r.instrumentolegalresoluciones_acta,
        "instrumentolegalresoluciones_ano": r.instrumentolegalresoluciones_ano,
        "instrumentolegalresoluciones_fecha_aprobacion": r.instrumentolegalresoluciones_fecha_aprobacion.isoformat(),
        "instrumentolegalresoluciones_descripcion": clip_value_html(r.instrumentolegalresoluciones_descripcion, 200),
        "instrumentolegalresoluciones_document": clip_value_html(r.instrumentolegalresoluciones_document or "", 200),
        "acciones": acciones,
    }


register_simple_datatable(
    router, InstrumentosLegalesResoluciones, "resoluciones-directorio",
    order_fields={**_RESOLUCION_ORDER_FIELDS, "instrumentolegalresoluciones_acta": "instrumentolegalresoluciones_acta"},
    filter_fields={
        **_RESOLUCION_FILTER_FIELDS,
        "instrumentolegalresoluciones_acta": "instrumentolegalresoluciones_acta__icontains",
    },
    search_lookups=[
        "instrumentolegalresoluciones_numero__icontains", "instrumentolegalresoluciones_acta__icontains",
        "instrumentolegalresoluciones_ano__icontains", "instrumentolegalresoluciones_descripcion__icontains",
        "instrumentolegalresoluciones_document__icontains",
    ],
    row_builder=_resolucion_directorio_datatable_row,
    default_order="-instrumentolegalresoluciones_ano,-instrumentolegalresoluciones_numero",
    queryset=InstrumentosLegalesResoluciones.objects.filter(instrumentolegalresoluciones_tipo="D"),
)


# --- MontoViaticoDiario ---
@router.get("/montos-viaticos/", response=List[MontoViaticoOut])
@decorate_view(require_model_perm(MontoViaticoDiario))
@paginate(PerPagePagination)
def list_montos_viaticos(request, decreto: str = ""):
    qs = MontoViaticoDiario.objects.select_related("montoviaticodiario_decreto_reglamentario").all().order_by("-id")
    if decreto:
        qs = qs.filter(montoviaticodiario_decreto_reglamentario_id=decreto)
    return qs


@router.post("/montos-viaticos/", response=MontoViaticoOut)
@decorate_view(require_model_perm(MontoViaticoDiario))
def create_monto_viatico(request, payload: MontoViaticoCreate):
    return MontoViaticoDiario.objects.create(**payload.model_dump())


@router.delete("/monto-viatico/{id}/")
@decorate_view(require_model_perm(MontoViaticoDiario))
def delete_monto_viatico(request, id: int):
    deleted, _ = MontoViaticoDiario.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Comisionado (personalizador.Agente) ---
@router.get("/comisionados/", response=List[ComisionadoOut])
@decorate_view(require_model_perm(Agente))
@paginate(PerPagePagination)
def list_comisionados(request, q: str = ""):
    qs = Agente.objects.select_related("sexo", "oficina").all().order_by("agente_apellidos")
    q = q.strip()
    if q:
        qs = qs.filter(Q(agente_nombres__icontains=q) | Q(agente_apellidos__icontains=q))
    return qs


@router.get("/comisionado/{id}/", response=ComisionadoOut)
@decorate_view(require_model_perm(Agente))
def retrieve_comisionado(request, id: int):
    return get_object_or_404(Agente, id=id)


@router.post("/comisionados/", response=ComisionadoOut)
@decorate_view(require_model_perm(Agente))
def create_comisionado(request, payload: ComisionadoCreate):
    return Agente.objects.create(**payload.model_dump())


@router.delete("/comisionado/{id}/")
@decorate_view(require_model_perm(Agente))
def delete_comisionado(request, id: int):
    deleted, _ = Agente.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Organigrama ---
@router.get("/organigramas/", response=List[OrganigramaOut])
@decorate_view(require_model_perm(Organigrama))
@paginate(PerPagePagination)
def list_organigramas(request):
    return Organigrama.objects.all().order_by("id")


@router.post("/organigramas/", response=OrganigramaOut)
@decorate_view(require_model_perm(Organigrama))
def create_organigrama(request, payload: OrganigramaCreate):
    return Organigrama.objects.create(**payload.model_dump())


@router.delete("/organigrama/{id}/")
@decorate_view(require_model_perm(Organigrama))
def delete_organigrama(request, id: int):
    deleted, _ = Organigrama.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Vehiculo ---
@router.get("/vehiculos/", response=List[VehiculoOut])
@decorate_view(require_model_perm(Vehiculo))
@paginate(PerPagePagination)
def list_vehiculos(request):
    return Vehiculo.objects.select_related(
        "vehiculo_poliza_aseguradora", "vehiculo_titular_agente", "vehiculo_titular_empresa"
    ).all().order_by("id")


@router.post("/vehiculos/", response=VehiculoOut)
@decorate_view(require_model_perm(Vehiculo))
def create_vehiculo(request, payload: VehiculoCreate):
    return Vehiculo.objects.create(**payload.model_dump())


@router.delete("/vehiculo/{id}/")
@decorate_view(require_model_perm(Vehiculo))
def delete_vehiculo(request, id: int):
    deleted, _ = Vehiculo.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


def _vehiculo_datatable_row(v: Vehiculo, user) -> dict:
    id_ = str(v.id)
    editarlink = f"<a href='/viaticos/crearvehiculo/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href=''>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/viaticos/eliminar/vehiculo/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("secretariador.delete_vehiculo"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("secretariador.change_vehiculo"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {
        "id": v.id,
        "vehiculo_caracter": v.get_vehiculo_caracter_display(),
        "vehiculo_modelo": v.vehiculo_modelo,
        "vehiculo_patente": v.vehiculo_patente,
        "vehiculo_poliza": v.vehiculo_poliza or "",
        "vehiculo_poliza_aseguradora": v.vehiculo_poliza_aseguradora.aseguradora_nombre if v.vehiculo_poliza_aseguradora_id else "",
        "acciones": acciones,
    }


register_simple_datatable(
    router, Vehiculo, "vehiculos",
    order_fields={
        "id": "id",
        "vehiculo_caracter": "vehiculo_caracter",
        "vehiculo_modelo": "vehiculo_modelo",
        "vehiculo_patente": "vehiculo_patente",
        "vehiculo_poliza": "vehiculo_poliza",
        "vehiculo_poliza_aseguradora": "vehiculo_poliza_aseguradora__aseguradora_nombre",
    },
    filter_fields={
        "vehiculo_caracter": "vehiculo_caracter",
        "vehiculo_modelo": "vehiculo_modelo__icontains",
        "vehiculo_patente": "vehiculo_patente__icontains",
        "vehiculo_poliza": "vehiculo_poliza__icontains",
        "vehiculo_poliza_aseguradora": "vehiculo_poliza_aseguradora__aseguradora_nombre__icontains",
    },
    search_lookups=[
        "vehiculo_modelo__icontains", "vehiculo_patente__icontains", "vehiculo_poliza__icontains",
        "vehiculo_poliza_aseguradora__aseguradora_nombre__icontains",
    ],
    row_builder=_vehiculo_datatable_row,
    default_order="vehiculo_modelo",
    queryset=Vehiculo.objects.select_related("vehiculo_poliza_aseguradora"),
)


# --- Solicitud (complex model with M2M) ---
@router.get("/solicitudes/", response=List[SolicitudOut])
@decorate_view(require_model_perm(Solicitud))
@paginate(PerPagePagination)
def list_solicitudes(request, provincia: str = ""):
    qs = Solicitud.objects.select_related("solicitud_solicitante", "solicitud_provincia").all().order_by("-id")
    if provincia:
        qs = qs.filter(solicitud_provincia_id=provincia)
    return qs


@router.get("/solicitud/{id}/", response=SolicitudOut)
@decorate_view(require_model_perm(Solicitud))
def retrieve_solicitud(request, id: int):
    return get_object_or_404(Solicitud, id=id)


@router.post("/solicitudes/", response=SolicitudOut)
@decorate_view(require_model_perm(Solicitud))
def create_solicitud(request, payload: SolicitudCreate):
    data = payload.model_dump()
    localidad_ids = data.pop("localidad_ids", None) or []
    s = Solicitud.objects.create(**data)
    if localidad_ids:
        s.solicitud_localidades.set(localidad_ids)
    return s


@router.delete("/solicitud/{id}/")
@decorate_view(require_model_perm(Solicitud))
def delete_solicitud(request, id: int):
    deleted, _ = Solicitud.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Solicitud datatable (server-side data for the DataTables listing) ---

_SOLICITUD_DATATABLE_ORDER_FIELDS = {
    "id": "id",
    "solicitud_actuacion_ano": "solicitud_actuacion_ano",
    "solicitud_actuacion_numero": "solicitud_actuacion_numero",
    "solicitud_solicitante": "solicitud_solicitante__agente_nombreyapellido",
    "solicitud_fecha_desde": "solicitud_fecha_desde",
    "solicitud_fecha_hasta": "solicitud_fecha_hasta",
    "solicitud_tareas": "solicitud_tareas",
    "solicitud_vehiculo": "solicitud_vehiculo__vehiculo_str",
    "solicitud_dia_inhabil": "solicitud_dia_inhabil",
}

_SOLICITUD_DATATABLE_FILTER_FIELDS = {
    "solicitud_actuacion_ano": "solicitud_actuacion_ano__icontains",
    "solicitud_actuacion_numero": "solicitud_actuacion_numero__icontains",
    "solicitud_solicitante": "solicitud_solicitante__agente_nombreyapellido__icontains",
    "Comisionados": "comisionadosolicitud__comisionadosolicitud_nombre__agente_nombreyapellido__icontains",
    "solicitud_localidades": "solicitud_localidades__localidad_nombre__icontains",
    "solicitud_tareas": "solicitud_tareas__icontains",
    "solicitud_vehiculo": "solicitud_vehiculo_id",
    "solicitud_dia_inhabil": "solicitud_dia_inhabil",
    "solicitud_fecha_desde": "solicitud_fecha_desde",
    "solicitud_fecha_hasta": "solicitud_fecha_hasta",
}

_SOLICITUD_DATATABLE_DISTINCT_FILTER_KEYS = {"solicitud_localidades", "Comisionados"}


def _solicitud_datatable_row(s: Solicitud, user) -> dict:
    id_ = str(s.id)
    if s.solicitud_provincia.provincia_nombre == "Chaco":
        editarlink = f"<a href='/viaticos/crearsolicitud/{id_}'>{editlinkimg}</a>"
        eliminarlink = f"<a href='/viaticos/eliminar/solicitud/{id_}'>{eliminarlinkimg}</a>"
        generarlink = f"<a href='/viaticos/creardocumento/solicitud/{id_}'>{generarlinkimg}</a>"
    else:
        editarlink = f"<a href='/viaticos/crearsolicitudexterior/{id_}'>{editlinkimg}</a>"
        eliminarlink = f"<a href='/viaticos/eliminar/solicitudexterior/{id_}'>{eliminarlinkimg}</a>"
        generarlink = f"<a href='/viaticos/creardocumento/solicitudexterior/{id_}'>{generarlinkimg}</a>"

    if s.solicitud_resolucion is not None:
        detallelink = f"<a href='{s.solicitud_resolucion.instrumentolegalresoluciones.url}'>{pdflinkimg}</a>"
    else:
        detallelink = ""

    if user.has_perm("secretariador.delete_solicitud"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}{generarlink}"
    elif user.has_perm("secretariador.change_solicitud"):
        acciones = f"{editarlink}{detallelink}{generarlink}"
    else:
        acciones = detallelink

    comisionados = "; ".join(
        c.comisionadosolicitud_nombre.agente_nombreyapellido for c in s.comisionadosolicitud_set.all()
    )

    return {
        "id": s.id,
        "solicitud_actuacion_ano": s.solicitud_actuacion_ano,
        "solicitud_actuacion_numero": s.solicitud_actuacion_numero,
        "solicitud_solicitante": s.solicitud_solicitante.agente_nombreyapellido,
        "Comisionados": comisionados,
        "solicitud_localidades": ", ".join(l.localidad_nombre for l in s.solicitud_localidades.all()),
        "solicitud_fecha_desde": s.solicitud_fecha_desde.isoformat(),
        "solicitud_fecha_hasta": s.solicitud_fecha_hasta.isoformat(),
        "solicitud_tareas": clip_value_html(s.solicitud_tareas, 100),
        "solicitud_vehiculo": s.solicitud_vehiculo.vehiculo_str if s.solicitud_vehiculo_id else "",
        "solicitud_dia_inhabil": "Sí" if s.solicitud_dia_inhabil else "No",
        "solicitud_anulada": s.solicitud_anulada,
        "acciones": acciones,
    }


@router.get("/datatables/solicitudes/")
@decorate_view(require_model_perm(Solicitud))
def datatable_solicitudes(
    request,
    draw: int = 1,
    start: int = 0,
    length: int = 50,
    search: str = "",
    order_by: str = "-solicitud_actuacion_ano,-solicitud_actuacion_numero",
    filters: str = "{}",
):
    qs = (
        Solicitud.objects.select_related(
            "solicitud_solicitante", "solicitud_provincia", "solicitud_vehiculo", "solicitud_resolucion"
        )
        .prefetch_related("solicitud_localidades", "comisionadosolicitud_set__comisionadosolicitud_nombre")
        .all()
    )
    records_total = qs.count()

    try:
        active_filters = json.loads(filters)
    except (TypeError, ValueError):
        active_filters = {}
    needs_distinct = False
    for key, value in active_filters.items():
        lookup = _SOLICITUD_DATATABLE_FILTER_FIELDS.get(key)
        if not lookup or value in (None, ""):
            continue
        if key == "solicitud_dia_inhabil":
            qs = qs.filter(**{lookup: value in ("true", "True", "1")})
        else:
            qs = qs.filter(**{lookup: value})
        if key in _SOLICITUD_DATATABLE_DISTINCT_FILTER_KEYS:
            needs_distinct = True
    if needs_distinct:
        qs = qs.distinct()

    if search:
        qs = qs.filter(
            Q(solicitud_actuacion_ano__icontains=search)
            | Q(solicitud_actuacion_numero__icontains=search)
            | Q(solicitud_solicitante__agente_nombreyapellido__icontains=search)
            | Q(comisionadosolicitud__comisionadosolicitud_nombre__agente_nombreyapellido__icontains=search)
            | Q(solicitud_localidades__localidad_nombre__icontains=search)
            | Q(solicitud_tareas__icontains=search)
            | Q(solicitud_vehiculo__vehiculo_str__icontains=search)
        ).distinct()

    records_filtered = qs.count()

    qs = qs.order_by(*parse_order_by(order_by, _SOLICITUD_DATATABLE_ORDER_FIELDS), "id")

    page = qs[start:] if length == -1 else qs[start:start + length]

    return {
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": [_solicitud_datatable_row(s, request.user) for s in page],
    }


@router.get("/datatables/solicitudes/{id}/detalle/")
@decorate_view(require_model_perm(Solicitud))
def datatable_solicitudes_detalle(request, id: int):
    s = get_object_or_404(
        Solicitud.objects.select_related("solicitud_provincia", "solicitud_decreto_viaticos", "solicitud_resolucion"),
        id=id,
    )
    html = render_to_string(
        "ajax_datatable/secretariador/solicitud/render_row_details.html",
        {"model": Solicitud, "object": s},
        request=request,
    )
    return {"html": html}


@router.get("/datatables/solicitudes/filtro-vehiculos/")
@decorate_view(require_model_perm(Solicitud))
def datatable_solicitudes_filtro_vehiculos(request):
    choices = (
        Solicitud.objects.exclude(solicitud_vehiculo=None)
        .values_list("solicitud_vehiculo_id", "solicitud_vehiculo__vehiculo_str")
        .distinct()
        .order_by("solicitud_vehiculo__vehiculo_str")
    )
    return {"choices": list(choices)}


# --- ComisionadoSolicitud ---
@router.get("/comisionados-solicitudes/", response=List[ComisionadoSolicitudOut])
@decorate_view(get_group_perms("dirgral_usuarios"), require_model_perm(ComisionadoSolicitud))
@paginate(PerPagePagination)
def list_comisionados_solicitudes(request, solicitud: str = ""):
    qs = ComisionadoSolicitud.objects.select_related("comisionadosolicitud_nombre").all().order_by("-id")
    if solicitud:
        qs = qs.filter(comisionadosolicitud_foreign_id=solicitud)
    return qs


@router.post("/comisionados-solicitudes/", response=ComisionadoSolicitudOut)
@decorate_view(require_model_perm(ComisionadoSolicitud))
def create_comisionado_solicitud(request, payload: ComisionadoSolicitudCreate):
    return ComisionadoSolicitud.objects.create(**payload.model_dump())


@router.delete("/comisionado-solicitud/{id}/")
@decorate_view(require_model_perm(ComisionadoSolicitud))
def delete_comisionado_solicitud(request, id: int):
    deleted, _ = ComisionadoSolicitud.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Incorporacion ---
@router.get("/incorporaciones/", response=List[IncorporacionOut])
@decorate_view(require_model_perm(Incorporacion))
@paginate(PerPagePagination)
def list_incorporaciones(request, solicitud: str = ""):
    qs = Incorporacion.objects.select_related("incorporacion_solicitud", "incorporacion_solicitante").all().order_by("-id")
    if solicitud:
        qs = qs.filter(incorporacion_solicitud_id=solicitud)
    return qs


@router.post("/incorporaciones/", response=IncorporacionOut)
@decorate_view(require_model_perm(Incorporacion))
def create_incorporacion(request, payload: IncorporacionCreate):
    return Incorporacion.objects.create(**payload.model_dump())


@router.delete("/incorporacion/{id}/")
@decorate_view(require_model_perm(Incorporacion))
def delete_incorporacion(request, id: int):
    deleted, _ = Incorporacion.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


def _incorporacion_datatable_row(i: Incorporacion, user) -> dict:
    id_ = str(i.id)
    editarlink = f"<a href='/viaticos/crearincorporacion/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href='/viaticos/crearincorporacion/ver/{id_}'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/viaticos/eliminar/incorporacion/{id_}'>{eliminarlinkimg}</a>"
    generarlink = f"<a href='/viaticos/creardocumento/incorporacion/{id_}'>{generarlinkimg}</a>"
    if user.has_perm("secretariador.delete_incorporacion"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}{generarlink}"
    elif user.has_perm("secretariador.change_incorporacion"):
        acciones = f"{editarlink}{detallelink}{generarlink}"
    else:
        acciones = detallelink
    return {
        "id": i.id,
        "incorporacion_actuacion_ano": i.incorporacion_actuacion_ano,
        "incorporacion_actuacion_numero": i.incorporacion_actuacion_numero,
        "incorporacion_solicitud": i.incorporacion_solicitud.solicitud_actuacion,
        "incorporacion_solicitante": i.incorporacion_solicitante.agente_nombreyapellido,
        "acciones": acciones,
    }


register_simple_datatable(
    router, Incorporacion, "incorporaciones",
    order_fields={
        "id": "id",
        "incorporacion_actuacion_ano": "incorporacion_actuacion_ano",
        "incorporacion_actuacion_numero": "incorporacion_actuacion_numero",
        "incorporacion_solicitud": "incorporacion_solicitud__solicitud_actuacion",
        "incorporacion_solicitante": "incorporacion_solicitante__agente_nombreyapellido",
    },
    filter_fields={
        "incorporacion_actuacion_ano": "incorporacion_actuacion_ano__icontains",
        "incorporacion_actuacion_numero": "incorporacion_actuacion_numero__icontains",
        "incorporacion_solicitud": "incorporacion_solicitud__solicitud_actuacion__icontains",
        "incorporacion_solicitante": "incorporacion_solicitante__agente_nombreyapellido__icontains",
    },
    search_lookups=[
        "incorporacion_actuacion_ano__icontains", "incorporacion_actuacion_numero__icontains",
        "incorporacion_solicitud__solicitud_actuacion__icontains",
        "incorporacion_solicitante__agente_nombreyapellido__icontains",
    ],
    row_builder=_incorporacion_datatable_row,
    default_order="-incorporacion_actuacion_ano,-incorporacion_actuacion_numero",
    queryset=Incorporacion.objects.select_related("incorporacion_solicitud", "incorporacion_solicitante"),
)
