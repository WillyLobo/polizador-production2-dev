# personalizador app API views
from typing import List

from django.contrib.auth import get_user_model
from django.db.models import BooleanField, Case, F, Func, IntegerField, Value, When
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
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
    LicenciaPermisoBalanceOut,
)
from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg
from personalizador.models import (
    Agente, ApartadoCargo, ActividadEspecifica, CargoTipo, Categoria, CEIC,
    ComisionadoExterno, Departamento, DenominacionCargo, Direccion, Directorio,
    Gerencia, GeneroAgente, GrupoCargo, Oficina, RepresentanteTecnico, TituloProfesional,
    LicenciaPermiso, PeriodoLicencia, TipoLicenciaPermiso,
)
from personalizador.licencias import (
    balance_tipo, resumen_agente, saldos_pendientes_agente,
    LICENCIA_IMPORTADA_MOTIVO_PREFIJO,
)

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
        "oficina": str(a.oficina) if a.oficina_id else "",
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
        "oficina": "oficina__cargo_gerencia__gerencia_nombre",
        "cuil": "cuil",
        "agente_personal_transitorio": "agente_personal_transitorio",
        "agente_personal_de_gabinete": "agente_personal_de_gabinete",
    },
    filter_fields={
        "agente_apellidos": "agente_apellidos__icontains",
        "agente_nombres": "agente_nombres__icontains",
        "oficina": "oficina__cargo_gerencia__gerencia_nombre__icontains",
        "cuil": "cuil__icontains",
        "agente_personal_transitorio": "agente_personal_transitorio",
        "agente_personal_de_gabinete": "agente_personal_de_gabinete",
    },
    search_lookups=[
        "agente_apellidos__icontains", "agente_nombres__icontains",
        "oficina__cargo_gerencia__gerencia_nombre__icontains", "cuil__icontains",
    ],
    row_builder=_agente_comisionado_datatable_row,
    default_order="agente_apellidos",
    queryset=Agente.objects.select_related(
        "oficina__cargo_directorio", "oficina__cargo_gerencia",
        "oficina__cargo_direccion", "oficina__cargo_departamento",
    ),
    boolean_filter_keys=frozenset({"agente_personal_transitorio", "agente_personal_de_gabinete"}),
)


# --- ComisionadoExterno datatable ---
def _comisionadoexterno_datatable_row(c: ComisionadoExterno, user) -> dict:
    id_ = str(c.id)
    editarlink = f"<a href='/viaticos/crearcomisionadoexterno/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href=''>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/viaticos/eliminar/comisionadoexterno/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("personalizador.delete_comisionadoexterno"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("personalizador.change_comisionadoexterno"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {
        "id": c.id,
        "agente_apellidos": c.agente_apellidos,
        "agente_nombres": c.agente_nombres,
        "institucion_origen": c.institucion_origen or "",
        "cuil": c.cuil,
        "acciones": acciones,
    }


register_simple_datatable(
    router, ComisionadoExterno, "comisionados-externos",
    order_fields={
        "id": "id",
        "agente_apellidos": "agente_apellidos",
        "agente_nombres": "agente_nombres",
        "institucion_origen": "institucion_origen",
        "cuil": "cuil",
    },
    filter_fields={
        "agente_apellidos": "agente_apellidos__icontains",
        "agente_nombres": "agente_nombres__icontains",
        "institucion_origen": "institucion_origen__icontains",
        "cuil": "cuil__icontains",
    },
    search_lookups=[
        "agente_apellidos__icontains", "agente_nombres__icontains",
        "institucion_origen__icontains", "cuil__icontains",
    ],
    row_builder=_comisionadoexterno_datatable_row,
    default_order="agente_apellidos",
    queryset=ComisionadoExterno.objects.select_related("sexo"),
)


def _simple_acciones(user, delete_perm, change_perm, editarlink, eliminarlink):
    if user.has_perm(delete_perm):
        return f"{editarlink}{eliminarlink}"
    elif user.has_perm(change_perm):
        return editarlink
    return ""


# --- GeneroAgente datatable ---
def _generoagente_datatable_row(g: GeneroAgente, user) -> dict:
    id_ = g.id
    acciones = _simple_acciones(
        user, "personalizador.delete_generoagente", "personalizador.change_generoagente",
        f"<a href='/personal/crear/generoagente/{id_}'>{editlinkimg}</a>",
        f"<a href='/personal/eliminar/generoagente/{id_}'>{eliminarlinkimg}</a>",
    )
    return {"id": g.id, "generoagente_nombre": g.generoagente_nombre, "acciones": acciones}


register_simple_datatable(
    router, GeneroAgente, "generoagentes",
    order_fields={"id": "id", "generoagente_nombre": "generoagente_nombre"},
    filter_fields={"generoagente_nombre": "generoagente_nombre__icontains"},
    search_lookups=["generoagente_nombre__icontains"],
    row_builder=_generoagente_datatable_row,
    default_order="generoagente_nombre",
)


# --- TituloProfesional datatable ---
def _tituloprofesional_datatable_row(t: TituloProfesional, user) -> dict:
    id_ = t.id
    acciones = _simple_acciones(
        user, "personalizador.delete_tituloprofesional", "personalizador.change_tituloprofesional",
        f"<a href='/personal/crear/tituloprofesional/{id_}'>{editlinkimg}</a>",
        f"<a href='/personal/eliminar/tituloprofesional/{id_}'>{eliminarlinkimg}</a>",
    )
    return {
        "id": t.id,
        "tituloprofesional_nombre": t.tituloprofesional_nombre,
        "tituloprofesional_abreviatura": t.tituloprofesional_abreviatura,
        "tituloprofesional_grado": t.tituloprofesional_grado,
        "acciones": acciones,
    }


register_simple_datatable(
    router, TituloProfesional, "tituloprofesionales",
    order_fields={
        "id": "id",
        "tituloprofesional_nombre": "tituloprofesional_nombre",
        "tituloprofesional_abreviatura": "tituloprofesional_abreviatura",
        "tituloprofesional_grado": "tituloprofesional_grado",
    },
    filter_fields={
        "tituloprofesional_nombre": "tituloprofesional_nombre__icontains",
        "tituloprofesional_abreviatura": "tituloprofesional_abreviatura__icontains",
        "tituloprofesional_grado": "tituloprofesional_grado__icontains",
    },
    search_lookups=["tituloprofesional_nombre__icontains", "tituloprofesional_abreviatura__icontains"],
    row_builder=_tituloprofesional_datatable_row,
    default_order="tituloprofesional_nombre",
)


# --- Categoria datatable ---
def _categoria_datatable_row(c: Categoria, user) -> dict:
    id_ = c.id
    acciones = _simple_acciones(
        user, "personalizador.delete_categoria", "personalizador.change_categoria",
        f"<a href='/personal/crear/categoria/{id_}'>{editlinkimg}</a>",
        f"<a href='/personal/eliminar/categoria/{id_}'>{eliminarlinkimg}</a>",
    )
    return {"id": c.id, "categoria_codigo": c.categoria_codigo, "categoria_nombre": c.categoria_nombre, "acciones": acciones}


register_simple_datatable(
    router, Categoria, "categorias",
    order_fields={"id": "id", "categoria_codigo": "categoria_codigo", "categoria_nombre": "categoria_nombre"},
    filter_fields={
        "categoria_codigo": "categoria_codigo",
        "categoria_nombre": "categoria_nombre__icontains",
    },
    search_lookups=["categoria_nombre__icontains"],
    row_builder=_categoria_datatable_row,
    default_order="categoria_nombre",
)


# --- DenominacionCargo datatable ---
def _denominacioncargo_datatable_row(d: DenominacionCargo, user) -> dict:
    id_ = d.id
    acciones = _simple_acciones(
        user, "personalizador.delete_denominacioncargo", "personalizador.change_denominacioncargo",
        f"<a href='/personal/crear/denominacioncargo/{id_}'>{editlinkimg}</a>",
        f"<a href='/personal/eliminar/denominacioncargo/{id_}'>{eliminarlinkimg}</a>",
    )
    return {"id": d.id, "denominacion": d.denominacion, "acciones": acciones}


register_simple_datatable(
    router, DenominacionCargo, "denominacioncargos",
    order_fields={"id": "id", "denominacion": "denominacion"},
    filter_fields={"denominacion": "denominacion__icontains"},
    search_lookups=["denominacion__icontains"],
    row_builder=_denominacioncargo_datatable_row,
    default_order="denominacion",
)


# --- ApartadoCargo datatable ---
def _apartadocargo_datatable_row(a: ApartadoCargo, user) -> dict:
    id_ = a.id
    acciones = _simple_acciones(
        user, "personalizador.delete_apartadocargo", "personalizador.change_apartadocargo",
        f"<a href='/personal/crear/apartadocargo/{id_}'>{editlinkimg}</a>",
        f"<a href='/personal/eliminar/apartadocargo/{id_}'>{eliminarlinkimg}</a>",
    )
    return {"id": a.id, "apartadocargo_denominacion": a.apartadocargo_denominacion, "acciones": acciones}


register_simple_datatable(
    router, ApartadoCargo, "apartadocargos",
    order_fields={"id": "id", "apartadocargo_denominacion": "apartadocargo_denominacion"},
    filter_fields={"apartadocargo_denominacion": "apartadocargo_denominacion__icontains"},
    search_lookups=["apartadocargo_denominacion__icontains"],
    row_builder=_apartadocargo_datatable_row,
    default_order="apartadocargo_denominacion",
)


# --- CEIC datatable ---
def _ceic_datatable_row(c: CEIC, user) -> dict:
    id_ = c.id
    acciones = _simple_acciones(
        user, "personalizador.delete_ceic", "personalizador.change_ceic",
        f"<a href='/personal/crear/ceic/{id_}'>{editlinkimg}</a>",
        f"<a href='/personal/eliminar/ceic/{id_}'>{eliminarlinkimg}</a>",
    )
    return {"id": c.id, "ceic": c.ceic, "acciones": acciones}


register_simple_datatable(
    router, CEIC, "ceics",
    order_fields={"id": "id", "ceic": "ceic"},
    filter_fields={"ceic": "ceic__icontains"},
    search_lookups=["ceic__icontains"],
    row_builder=_ceic_datatable_row,
    default_order="ceic",
)


# --- GrupoCargo datatable ---
def _grupocargo_datatable_row(g: GrupoCargo, user) -> dict:
    id_ = g.id
    acciones = _simple_acciones(
        user, "personalizador.delete_grupocargo", "personalizador.change_grupocargo",
        f"<a href='/personal/crear/grupocargo/{id_}'>{editlinkimg}</a>",
        f"<a href='/personal/eliminar/grupocargo/{id_}'>{eliminarlinkimg}</a>",
    )
    return {"id": g.id, "grupo_numero": g.grupo_numero, "acciones": acciones}


register_simple_datatable(
    router, GrupoCargo, "grupocargos",
    order_fields={"id": "id", "grupo_numero": "grupo_numero"},
    filter_fields={"grupo_numero": "grupo_numero"},
    search_lookups=[],
    row_builder=_grupocargo_datatable_row,
    default_order="grupo_numero",
)


# --- ActividadEspecifica datatable ---
def _actividadespecifica_datatable_row(a: ActividadEspecifica, user) -> dict:
    id_ = a.id
    acciones = _simple_acciones(
        user, "personalizador.delete_actividadespecifica", "personalizador.change_actividadespecifica",
        f"<a href='/personal/crear/actividadespecifica/{id_}'>{editlinkimg}</a>",
        f"<a href='/personal/eliminar/actividadespecifica/{id_}'>{eliminarlinkimg}</a>",
    )
    return {
        "id": a.id,
        "actividad_especifica_codigo": a.actividad_especifica_codigo,
        "actividad_especifica_nombre": a.actividad_especifica_nombre,
        "acciones": acciones,
    }


register_simple_datatable(
    router, ActividadEspecifica, "actividadespecificas",
    order_fields={
        "id": "id",
        "actividad_especifica_codigo": "actividad_especifica_codigo",
        "actividad_especifica_nombre": "actividad_especifica_nombre",
    },
    filter_fields={
        "actividad_especifica_codigo": "actividad_especifica_codigo",
        "actividad_especifica_nombre": "actividad_especifica_nombre__icontains",
    },
    search_lookups=["actividad_especifica_nombre__icontains"],
    row_builder=_actividadespecifica_datatable_row,
    default_order="actividad_especifica_nombre",
)


# --- CargoTipo datatable ---
def _cargotipo_datatable_row(c: CargoTipo, user) -> dict:
    id_ = c.id
    acciones = _simple_acciones(
        user, "personalizador.delete_cargotipo", "personalizador.change_cargotipo",
        f"<a href='/personal/crear/cargotipo/{id_}'>{editlinkimg}</a>",
        f"<a href='/personal/eliminar/cargotipo/{id_}'>{eliminarlinkimg}</a>",
    )
    return {"id": c.id, "cargotipo": c.cargotipo, "acciones": acciones}


register_simple_datatable(
    router, CargoTipo, "cargotipos",
    order_fields={"id": "id", "cargotipo": "cargotipo"},
    filter_fields={"cargotipo": "cargotipo__icontains"},
    search_lookups=["cargotipo__icontains"],
    row_builder=_cargotipo_datatable_row,
    default_order="cargotipo",
)


# --- Directorio datatable ---
def _directorio_datatable_row(d: Directorio, user) -> dict:
    id_ = d.id
    acciones = _simple_acciones(
        user, "personalizador.delete_directorio", "personalizador.change_directorio",
        f"<a href='/personal/crear/directorio/{id_}'>{editlinkimg}</a>",
        f"<a href='/personal/eliminar/directorio/{id_}'>{eliminarlinkimg}</a>",
    )
    return {
        "id": d.id,
        "directorio_nombre": d.directorio_nombre,
        "directorio_autoridad_a_cargo": d.directorio_autoridad_a_cargo or "",
        "directorio_cuof": d.directorio_cuof,
        "acciones": acciones,
    }


register_simple_datatable(
    router, Directorio, "directorios",
    order_fields={
        "id": "id",
        "directorio_nombre": "directorio_nombre",
        "directorio_autoridad_a_cargo": "directorio_autoridad_a_cargo",
        "directorio_cuof": "directorio_cuof",
    },
    filter_fields={
        "directorio_nombre": "directorio_nombre__icontains",
        "directorio_cuof": "directorio_cuof__icontains",
    },
    search_lookups=["directorio_nombre__icontains", "directorio_cuof__icontains"],
    row_builder=_directorio_datatable_row,
    default_order="directorio_nombre",
)


# --- Gerencia (personalizador) datatable ---
def _gerencia_personal_datatable_row(g: Gerencia, user) -> dict:
    id_ = g.id
    acciones = _simple_acciones(
        user, "personalizador.delete_gerencia", "personalizador.change_gerencia",
        f"<a href='/personal/crear/gerencia/{id_}'>{editlinkimg}</a>",
        f"<a href='/personal/eliminar/gerencia/{id_}'>{eliminarlinkimg}</a>",
    )
    return {
        "id": g.id,
        "gerencia_nombre": g.gerencia_nombre,
        "gerencia_directorio": g.gerencia_directorio.directorio_nombre if g.gerencia_directorio_id else "",
        "gerencia_cuof": g.gerencia_cuof,
        "acciones": acciones,
    }


register_simple_datatable(
    router, Gerencia, "gerencias",
    order_fields={
        "id": "id",
        "gerencia_nombre": "gerencia_nombre",
        "gerencia_directorio": "gerencia_directorio__directorio_nombre",
        "gerencia_cuof": "gerencia_cuof",
    },
    filter_fields={
        "gerencia_nombre": "gerencia_nombre__icontains",
        "gerencia_directorio": "gerencia_directorio__directorio_nombre__icontains",
        "gerencia_cuof": "gerencia_cuof__icontains",
    },
    search_lookups=["gerencia_nombre__icontains", "gerencia_cuof__icontains"],
    row_builder=_gerencia_personal_datatable_row,
    default_order="gerencia_nombre",
    queryset=Gerencia.objects.select_related("gerencia_directorio"),
)


# --- Direccion (personalizador) datatable ---
def _direccion_personal_datatable_row(d: Direccion, user) -> dict:
    id_ = d.id
    acciones = _simple_acciones(
        user, "personalizador.delete_direccion", "personalizador.change_direccion",
        f"<a href='/personal/crear/direccion/{id_}'>{editlinkimg}</a>",
        f"<a href='/personal/eliminar/direccion/{id_}'>{eliminarlinkimg}</a>",
    )
    return {
        "id": d.id,
        "direccion_nombre": d.direccion_nombre,
        "direccion_gerencia": d.direccion_gerencia.gerencia_nombre if d.direccion_gerencia_id else "",
        "direccion_cuof": d.direccion_cuof,
        "acciones": acciones,
    }


register_simple_datatable(
    router, Direccion, "direcciones",
    order_fields={
        "id": "id",
        "direccion_nombre": "direccion_nombre",
        "direccion_gerencia": "direccion_gerencia__gerencia_nombre",
        "direccion_cuof": "direccion_cuof",
    },
    filter_fields={
        "direccion_nombre": "direccion_nombre__icontains",
        "direccion_gerencia": "direccion_gerencia__gerencia_nombre__icontains",
        "direccion_cuof": "direccion_cuof__icontains",
    },
    search_lookups=["direccion_nombre__icontains", "direccion_cuof__icontains"],
    row_builder=_direccion_personal_datatable_row,
    default_order="direccion_nombre",
    queryset=Direccion.objects.select_related("direccion_gerencia"),
)


# --- Departamento (personalizador) datatable ---
def _departamento_personal_datatable_row(d: Departamento, user) -> dict:
    id_ = d.id
    acciones = _simple_acciones(
        user, "personalizador.delete_departamento", "personalizador.change_departamento",
        f"<a href='/personal/crear/departamento/{id_}'>{editlinkimg}</a>",
        f"<a href='/personal/eliminar/departamento/{id_}'>{eliminarlinkimg}</a>",
    )
    return {
        "id": d.id,
        "departamento_nombre": d.departamento_nombre,
        "departamento_direccion": d.departamento_direccion.direccion_nombre if d.departamento_direccion_id else "",
        "departamento_cuof": d.departamento_cuof,
        "acciones": acciones,
    }


register_simple_datatable(
    router, Departamento, "departamentos-personal",
    order_fields={
        "id": "id",
        "departamento_nombre": "departamento_nombre",
        "departamento_direccion": "departamento_direccion__direccion_nombre",
        "departamento_cuof": "departamento_cuof",
    },
    filter_fields={
        "departamento_nombre": "departamento_nombre__icontains",
        "departamento_direccion": "departamento_direccion__direccion_nombre__icontains",
        "departamento_cuof": "departamento_cuof__icontains",
    },
    search_lookups=["departamento_nombre__icontains", "departamento_cuof__icontains"],
    row_builder=_departamento_personal_datatable_row,
    default_order="departamento_nombre",
    queryset=Departamento.objects.select_related("departamento_direccion"),
)


# --- Oficina datatable ---
def _oficina_datatable_row(o: Oficina, user) -> dict:
    id_ = o.id
    acciones = _simple_acciones(
        user, "personalizador.delete_oficina", "personalizador.change_oficina",
        f"<a href='/personal/crear/oficina/{id_}'>{editlinkimg}</a>",
        f"<a href='/personal/eliminar/oficina/{id_}'>{eliminarlinkimg}</a>",
    )
    return {
        "id": o.id,
        "cargo_directorio": o.cargo_directorio.directorio_nombre if o.cargo_directorio_id else "",
        "cargo_gerencia": o.cargo_gerencia.gerencia_nombre if o.cargo_gerencia_id else "",
        "cargo_direccion": o.cargo_direccion.direccion_nombre if o.cargo_direccion_id else "",
        "cargo_departamento": o.cargo_departamento.departamento_nombre if o.cargo_departamento_id else "",
        "acciones": acciones,
    }


register_simple_datatable(
    router, Oficina, "oficinas",
    order_fields={
        "id": "id",
        "cargo_directorio": "cargo_directorio__directorio_nombre",
        "cargo_gerencia": "cargo_gerencia__gerencia_nombre",
        "cargo_direccion": "cargo_direccion__direccion_nombre",
        "cargo_departamento": "cargo_departamento__departamento_nombre",
    },
    filter_fields={
        "cargo_directorio": "cargo_directorio__directorio_nombre__icontains",
        "cargo_gerencia": "cargo_gerencia__gerencia_nombre__icontains",
        "cargo_direccion": "cargo_direccion__direccion_nombre__icontains",
        "cargo_departamento": "cargo_departamento__departamento_nombre__icontains",
    },
    search_lookups=[
        "cargo_directorio__directorio_nombre__icontains", "cargo_gerencia__gerencia_nombre__icontains",
        "cargo_direccion__direccion_nombre__icontains", "cargo_departamento__departamento_nombre__icontains",
    ],
    row_builder=_oficina_datatable_row,
    default_order="id",
    queryset=Oficina.objects.select_related("cargo_directorio", "cargo_gerencia", "cargo_direccion", "cargo_departamento"),
)


# --- Agente (management list) datatable ---
class _EdadCalculada(Func):
    """Años completos entre hoy y `fecha_nacimiento`, calculado en Postgres:
    EXTRACT(YEAR FROM AGE(fecha_nacimiento))."""
    template = "EXTRACT(YEAR FROM AGE(%(expressions)s))"
    output_field = IntegerField()


def _formatear_antiguedad(antiguedad: dict | None) -> str:
    if not antiguedad:
        return ""
    return f"{antiguedad['anios']}a {antiguedad['meses']}m {antiguedad['dias']}d"


def _agente_datatable_row(a: Agente, user) -> dict:
    id_ = a.id
    editarlink = f"<a href='/personal/crear/agente/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href='/personal/agente/ficha/{id_}'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/personal/eliminar/agente/{id_}'>{eliminarlinkimg}</a>"
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
        "dni": a.dni,
        "denominacion": a.denominacion_cargo.denominacion if a.denominacion_cargo_id else "",
        "oficina": str(a.oficina) if a.oficina_id else "",
        "edad": int(a.edad_calculada) if a.edad_calculada is not None else "",
        "antiguedad": _formatear_antiguedad(a.antiguedad),
        "activo": "Sí" if a.activo else "No",
        "con_errores": "Sí" if a.con_errores else "No",
        "acciones": acciones,
    }


register_simple_datatable(
    router, Agente, "agentes",
    order_fields={
        "id": "id",
        "agente_apellidos": "agente_apellidos",
        "agente_nombres": "agente_nombres",
        "dni": "dni",
        "denominacion": "denominacion_cargo__denominacion",
        "edad": "edad_calculada",
        "activo": "activo",
        "con_errores": "con_errores",
    },
    filter_fields={
        "agente_apellidos": "agente_apellidos__icontains",
        "agente_nombres": "agente_nombres__icontains",
        "dni": "dni__icontains",
        "denominacion": "denominacion_cargo_id",
        "edad": "edad_calculada",
        "activo": "activo",
        "con_errores": "con_errores",
    },
    search_lookups=["agente_apellidos__icontains", "agente_nombres__icontains", "dni__icontains"],
    row_builder=_agente_datatable_row,
    default_order="agente_apellidos",
    queryset=Agente.objects.select_related(
        "denominacion_cargo", "oficina__cargo_directorio", "oficina__cargo_gerencia",
        "oficina__cargo_direccion", "oficina__cargo_departamento",
    ).annotate(edad_calculada=_EdadCalculada(F("fecha_nacimiento"))),
    boolean_filter_keys=frozenset({"activo", "con_errores"}),
    with_detail=False,
)


@router.get("/datatables/agentes/{id}/detalle/")
@decorate_view(require_model_perm(Agente))
def datatable_agentes_detalle(request, id: int):
    agente = get_object_or_404(
        Agente.objects.select_related(
            "sexo", "categoria", "denominacion_cargo", "apartado", "ceic", "grupo",
            "actividad_especifica", "domicilio_localidad", "domicilio_provincia",
            "oficina__cargo_directorio", "oficina__cargo_gerencia",
            "oficina__cargo_direccion", "oficina__cargo_departamento",
            "cargo_interno__cargo_directorio", "cargo_interno__cargo_gerencia",
            "cargo_interno__cargo_direccion", "cargo_interno__cargo_departamento",
        ).prefetch_related("titulo_profesional", "licenciapermiso_set__licenciapermiso_tipo"),
        id=id,
    )
    anio = timezone.now().year
    html = render_to_string(
        "ajax_datatable/personalizador/agente/render_row_details.html",
        {
            "object": agente,
            "anio": anio,
            "resumen": resumen_agente(agente, anio),
            "saldos_pendientes": saldos_pendientes_agente(agente),
            "licencias_recientes": agente.licenciapermiso_set.all()[:10],
        },
        request=request,
    )
    return {"html": html}


@router.get("/datatables/agentes/filtro-denominacion/")
@decorate_view(require_model_perm(Agente))
def datatable_agentes_filtro_denominacion(request):
    choices = (
        Agente.objects.exclude(denominacion_cargo=None)
        .values_list("denominacion_cargo_id", "denominacion_cargo__denominacion")
        .distinct()
        .order_by("denominacion_cargo__denominacion")
    )
    return {"choices": list(choices)}


# --- LicenciaPermiso datatable ---
def _licenciapermiso_datatable_row(s: LicenciaPermiso, user) -> dict:
    id_ = s.id
    verlink = f"<a href='/personal/licencias/ver/{id_}'>{detallelinkimg}</a>"
    acciones = verlink
    if user.has_perm("personalizador.change_licenciapermiso"):
        acciones += f"<a href='/personal/licencias/crear/{id_}'>{editlinkimg}</a>"
    if user.has_perm("personalizador.delete_licenciapermiso"):
        acciones += f"<a href='/personal/licencias/eliminar/{id_}'>{eliminarlinkimg}</a>"
    return {
        "id": s.id,
        "licenciapermiso_agente": str(s.licenciapermiso_agente),
        "licenciapermiso_tipo": s.licenciapermiso_tipo.tipolicenciapermiso_nombre,
        "licenciapermiso_fecha_desde": s.licenciapermiso_fecha_desde,
        "licenciapermiso_fecha_hasta": s.licenciapermiso_fecha_hasta,
        "licenciapermiso_cantidad": s.licenciapermiso_cantidad,
        "licenciapermiso_anulada": "Sí" if s.licenciapermiso_anulada else "No",
        "licenciapermiso_importada": "Sí" if s.licenciapermiso_importada else "No",
        "acciones": acciones,
    }


register_simple_datatable(
    router, LicenciaPermiso, "licenciapermisos",
    order_fields={
        "id": "id",
        "licenciapermiso_agente": "licenciapermiso_agente__agente_apellidos",
        "licenciapermiso_tipo": "licenciapermiso_tipo__tipolicenciapermiso_nombre",
        "licenciapermiso_fecha_desde": "licenciapermiso_fecha_desde",
        "licenciapermiso_fecha_hasta": "licenciapermiso_fecha_hasta",
        "licenciapermiso_anulada": "licenciapermiso_anulada",
        "licenciapermiso_importada": "licenciapermiso_importada",
    },
    filter_fields={
        "licenciapermiso_agente": "licenciapermiso_agente__agente_apellidos__icontains",
        "licenciapermiso_tipo": "licenciapermiso_tipo__tipolicenciapermiso_nombre__icontains",
        "licenciapermiso_anulada": "licenciapermiso_anulada",
        "licenciapermiso_importada": "licenciapermiso_importada",
    },
    search_lookups=[
        "licenciapermiso_agente__agente_apellidos__icontains",
        "licenciapermiso_agente__agente_nombres__icontains",
        "licenciapermiso_tipo__tipolicenciapermiso_nombre__icontains",
    ],
    row_builder=_licenciapermiso_datatable_row,
    default_order="-licenciapermiso_fecha_desde",
    queryset=LicenciaPermiso.objects.select_related("licenciapermiso_agente", "licenciapermiso_tipo").annotate(
        licenciapermiso_importada=Case(
            When(licenciapermiso_motivo__startswith=LICENCIA_IMPORTADA_MOTIVO_PREFIJO, then=Value(True)),
            default=Value(False), output_field=BooleanField(),
        ),
    ),
    boolean_filter_keys=frozenset({"licenciapermiso_anulada", "licenciapermiso_importada"}),
)


# --- TipoLicenciaPermiso datatable ---
def _tipolicenciapermiso_datatable_row(t: TipoLicenciaPermiso, user) -> dict:
    id_ = t.id
    acciones = _simple_acciones(
        user, "personalizador.delete_tipolicenciapermiso", "personalizador.change_tipolicenciapermiso",
        f"<a href='/personal/crear/tipolicenciapermiso/{id_}'>{editlinkimg}</a>",
        f"<a href='/personal/eliminar/tipolicenciapermiso/{id_}'>{eliminarlinkimg}</a>",
    )
    if t.tipolicenciapermiso_tope_cantidad is not None:
        tope = f"{t.tipolicenciapermiso_tope_cantidad} ({t.get_tipolicenciapermiso_tope_periodo_display()})"
    else:
        tope = "Variable"
    return {
        "id": t.id,
        "tipolicenciapermiso_articulo": t.tipolicenciapermiso_articulo,
        "tipolicenciapermiso_nombre": t.tipolicenciapermiso_nombre,
        "tipolicenciapermiso_categoria": t.get_tipolicenciapermiso_categoria_display(),
        "tipolicenciapermiso_unidad": t.get_tipolicenciapermiso_unidad_display(),
        "tipolicenciapermiso_tope": tope,
        "tipolicenciapermiso_remunerada": t.get_tipolicenciapermiso_remunerada_display(),
        "tipolicenciapermiso_activo": "Sí" if t.tipolicenciapermiso_activo else "No",
        "acciones": acciones,
    }


register_simple_datatable(
    router, TipoLicenciaPermiso, "tipolicenciapermisos",
    order_fields={
        "id": "id",
        "tipolicenciapermiso_articulo": "tipolicenciapermiso_articulo",
        "tipolicenciapermiso_nombre": "tipolicenciapermiso_nombre",
        "tipolicenciapermiso_categoria": "tipolicenciapermiso_categoria",
        "tipolicenciapermiso_unidad": "tipolicenciapermiso_unidad",
        "tipolicenciapermiso_remunerada": "tipolicenciapermiso_remunerada",
        "tipolicenciapermiso_activo": "tipolicenciapermiso_activo",
    },
    filter_fields={
        "tipolicenciapermiso_articulo": "tipolicenciapermiso_articulo__icontains",
        "tipolicenciapermiso_nombre": "tipolicenciapermiso_nombre__icontains",
        "tipolicenciapermiso_categoria": "tipolicenciapermiso_categoria",
        "tipolicenciapermiso_activo": "tipolicenciapermiso_activo",
    },
    search_lookups=[
        "tipolicenciapermiso_nombre__icontains",
        "tipolicenciapermiso_articulo__icontains",
    ],
    row_builder=_tipolicenciapermiso_datatable_row,
    default_order="tipolicenciapermiso_categoria",
    boolean_filter_keys=frozenset({"tipolicenciapermiso_activo"}),
)


# --- PeriodoLicencia datatable ---
def _periodolicencia_datatable_row(p: PeriodoLicencia, user) -> dict:
    id_ = p.id
    acciones = _simple_acciones(
        user, "personalizador.delete_periodolicencia", "personalizador.change_periodolicencia",
        f"<a href='/personal/licencias/periodos/crear/{id_}'>{editlinkimg}</a>",
        f"<a href='/personal/licencias/periodos/eliminar/{id_}'>{eliminarlinkimg}</a>",
    )
    if p.periodolicencia_categoria == "LOR_ANUAL":
        turno1, turno2 = "—", "—"
    else:
        turno1 = f"{p.periodolicencia_turno1_desde} al {p.periodolicencia_turno1_hasta}"
        turno2 = f"{p.periodolicencia_turno2_desde} al {p.periodolicencia_turno2_hasta}"
    return {
        "id": p.id,
        "periodolicencia_categoria": p.get_periodolicencia_categoria_display(),
        "periodolicencia_anio": p.periodolicencia_anio,
        "periodolicencia_apertura": p.periodolicencia_apertura or "—",
        "periodolicencia_fecha_limite_solicitud": p.periodolicencia_fecha_limite_solicitud or "—",
        "periodolicencia_turno1": turno1,
        "periodolicencia_turno2": turno2,
        "acciones": acciones,
    }


register_simple_datatable(
    router, PeriodoLicencia, "periodolicencias",
    order_fields={
        "id": "id",
        "periodolicencia_categoria": "periodolicencia_categoria",
        "periodolicencia_anio": "periodolicencia_anio",
    },
    filter_fields={
        "periodolicencia_categoria": "periodolicencia_categoria",
        "periodolicencia_anio": "periodolicencia_anio",
    },
    search_lookups=[],
    row_builder=_periodolicencia_datatable_row,
    default_order="-periodolicencia_anio",
)


@router.get("/licenciapermiso-balance/", response=LicenciaPermisoBalanceOut)
@decorate_view(require_model_perm(LicenciaPermiso))
def licenciapermiso_balance(request, agente: int, tipo: int, anio: int = None):
    """Días/horas correspondientes, usados y disponibles de `tipo` para `agente` en
    `anio` (año actual por defecto). Para la Licencia Anual Ordinaria, `correspondientes`
    ya viene calculado según la antigüedad del agente (ver `licencias.balance_tipo`)."""
    agente_obj = get_object_or_404(Agente, pk=agente)
    tipo_obj = get_object_or_404(TipoLicenciaPermiso, pk=tipo)
    balance = balance_tipo(agente_obj, tipo_obj, anio or timezone.now().year)
    return {
        "unidad": tipo_obj.tipolicenciapermiso_unidad,
        "unidad_display": tipo_obj.get_tipolicenciapermiso_unidad_display(),
        "correspondientes": balance["correspondientes"],
        "usados": balance["usados"],
        "disponibles": balance["disponibles"],
    }
