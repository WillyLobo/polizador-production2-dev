# secretariador app API views
from typing import List

from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.decorators import decorate_view
from ninja.pagination import paginate

from api.permissions import get_group_perms, require_model_perm
from api.views.generics import PerPagePagination
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
