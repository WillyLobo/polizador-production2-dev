# personalizador app API views
from typing import List

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.decorators import decorate_view
from ninja.pagination import paginate

from api.permissions import require_model_perm
from api.views.generics import PerPagePagination, register_simple_datatable
from api.schemas.personalizador_schemas import (
    CustomUserOut,
    GerenciaOut, GerenciaCreate,
    DireccionOut, DireccionCreate,
    DepartamentoPerOut, DepartamentoPerCreate,
)
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg
from personalizador.models import Agente, Departamento, Direccion, Gerencia, RepresentanteTecnico

User = get_user_model()
router = Router(tags=["personalizador"])


# --- CustomUser ---
@router.get("/users/", response=List[CustomUserOut])
@decorate_view(require_model_perm(User))
@paginate(PerPagePagination)
def list_users(request):
    return User.objects.all().order_by("username")


@router.get("/user/{id}/", response=CustomUserOut)
@decorate_view(require_model_perm(User))
def retrieve_user(request, id: int):
    return get_object_or_404(User, id=id)


# --- Gerencia ---
@router.get("/gerencias/", response=List[GerenciaOut])
@decorate_view(require_model_perm(Gerencia))
@paginate(PerPagePagination)
def list_gerencias(request):
    return Gerencia.objects.all().order_by("id")


@router.post("/gerencias/", response=GerenciaOut)
@decorate_view(require_model_perm(Gerencia))
def create_gerencia(request, payload: GerenciaCreate):
    return Gerencia.objects.create(**payload.model_dump())


@router.delete("/gerencia/{id}/")
@decorate_view(require_model_perm(Gerencia))
def delete_gerencia(request, id: int):
    deleted, _ = Gerencia.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Direccion ---
@router.get("/direcciones/", response=List[DireccionOut])
@decorate_view(require_model_perm(Direccion))
@paginate(PerPagePagination)
def list_direcciones(request):
    return Direccion.objects.all().order_by("id")


@router.post("/direcciones/", response=DireccionOut)
@decorate_view(require_model_perm(Direccion))
def create_direccion(request, payload: DireccionCreate):
    return Direccion.objects.create(**payload.model_dump())


@router.delete("/direccion/{id}/")
@decorate_view(require_model_perm(Direccion))
def delete_direccion(request, id: int):
    deleted, _ = Direccion.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Departamento (personalizador) ---
@router.get("/departamentos-personal/", response=List[DepartamentoPerOut])
@decorate_view(require_model_perm(Departamento))
@paginate(PerPagePagination)
def list_departamentos_personal(request):
    return Departamento.objects.all().order_by("id")


@router.post("/departamentos-personal/", response=DepartamentoPerOut)
@decorate_view(require_model_perm(Departamento))
def create_departamento_personal(request, payload: DepartamentoPerCreate):
    return Departamento.objects.create(**payload.model_dump())


@router.delete("/departamento-personal/{id}/")
@decorate_view(require_model_perm(Departamento))
def delete_departamento_personal(request, id: int):
    deleted, _ = Departamento.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- RepresentanteTecnico datatable ---
def _representantetecnico_datatable_row(r: RepresentanteTecnico, user) -> dict:
    id_ = str(r.id)
    editarlink = f"<a href='/obra/crear/representantetecnico/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href='/obra/crear/representantetecnico/obra/{id_}'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/obra/eliminar/representantetecnico/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("personalizador.delete_representantetecnico"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("personalizador.change_representantetecnico"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {
        "id": r.id,
        "representantetecnico_nombre": r.representantetecnico_nombre,
        "representantetecnico_apellido": r.representantetecnico_apellido,
        "representantetecnico_dni": r.representantetecnico_dni,
        "representantetecnico_cuil": r.representantetecnico_cuil,
        "representantetecnico_profesion": r.representantetecnico_profesion.tituloprofesional_nombre,
        "representantetecnico_matricula": r.representantetecnico_matricula,
        "acciones": acciones,
    }


register_simple_datatable(
    router, RepresentanteTecnico, "representantes-tecnicos",
    order_fields={
        "id": "id",
        "representantetecnico_nombre": "representantetecnico_nombre",
        "representantetecnico_apellido": "representantetecnico_apellido",
        "representantetecnico_dni": "representantetecnico_dni",
        "representantetecnico_cuil": "representantetecnico_cuil",
        "representantetecnico_profesion": "representantetecnico_profesion__tituloprofesional_nombre",
        "representantetecnico_matricula": "representantetecnico_matricula",
    },
    filter_fields={
        "representantetecnico_nombre": "representantetecnico_nombre__icontains",
        "representantetecnico_apellido": "representantetecnico_apellido__icontains",
        "representantetecnico_dni": "representantetecnico_dni__icontains",
        "representantetecnico_cuil": "representantetecnico_cuil__icontains",
        "representantetecnico_profesion": "representantetecnico_profesion__tituloprofesional_nombre__icontains",
        "representantetecnico_matricula": "representantetecnico_matricula__icontains",
    },
    search_lookups=[
        "representantetecnico_nombre__icontains", "representantetecnico_apellido__icontains",
        "representantetecnico_dni__icontains", "representantetecnico_cuil__icontains",
        "representantetecnico_profesion__tituloprofesional_nombre__icontains",
        "representantetecnico_matricula__icontains",
    ],
    row_builder=_representantetecnico_datatable_row,
    queryset=RepresentanteTecnico.objects.select_related("representantetecnico_profesion"),
)


# --- Agente (Comisionados) datatable ---
def _agente_comisionado_datatable_row(a: Agente, user) -> dict:
    id_ = str(a.id)
    editarlink = f"<a href='/viaticos/crearcomisionado/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href=''>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/viaticos/eliminar/comisionado/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("personalizador.delete_agente"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("personalizador.change_agente"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {
        "id": a.id,
        "agente_apellidos": a.agente_apellidos,
        "agente_nombres": a.agente_nombres,
        "oficina": a.oficina.cargo_tipo.cargotipo if a.oficina_id else "",
        "cuil": a.cuil,
        "agente_personal_transitorio": "Sí" if a.agente_personal_transitorio else "No",
        "agente_personal_de_gabinete": "Sí" if a.agente_personal_de_gabinete else "No",
        "acciones": acciones,
    }


register_simple_datatable(
    router, Agente, "comisionados",
    order_fields={
        "id": "id",
        "agente_apellidos": "agente_apellidos",
        "agente_nombres": "agente_nombres",
        "oficina": "oficina__cargo_tipo__cargotipo",
        "cuil": "cuil",
        "agente_personal_transitorio": "agente_personal_transitorio",
        "agente_personal_de_gabinete": "agente_personal_de_gabinete",
    },
    filter_fields={
        "agente_apellidos": "agente_apellidos__icontains",
        "agente_nombres": "agente_nombres__icontains",
        "oficina": "oficina__cargo_tipo__cargotipo__icontains",
        "cuil": "cuil__icontains",
        "agente_personal_transitorio": "agente_personal_transitorio",
        "agente_personal_de_gabinete": "agente_personal_de_gabinete",
    },
    search_lookups=[
        "agente_apellidos__icontains", "agente_nombres__icontains",
        "oficina__cargo_tipo__cargotipo__icontains", "cuil__icontains",
    ],
    row_builder=_agente_comisionado_datatable_row,
    default_order="agente_apellidos",
    queryset=Agente.objects.select_related("oficina__cargo_tipo"),
    boolean_filter_keys=frozenset({"agente_personal_transitorio", "agente_personal_de_gabinete"}),
)
