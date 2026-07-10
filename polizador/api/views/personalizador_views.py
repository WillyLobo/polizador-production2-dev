# personalizador app API views
from typing import List

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.decorators import decorate_view
from ninja.pagination import paginate

from api.permissions import require_model_perm
from api.views.generics import PerPagePagination
from api.schemas.personalizador_schemas import (
    CustomUserOut,
    GerenciaOut, GerenciaCreate,
    DireccionOut, DireccionCreate,
    DepartamentoPerOut, DepartamentoPerCreate,
)
from personalizador.models import Departamento, Direccion, Gerencia

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
