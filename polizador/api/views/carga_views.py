# carga app API views
import json
from typing import List

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from ninja import Router
from ninja.decorators import decorate_view
from ninja.pagination import paginate

from polizador.vars import editlinkimg, detallelinkimg, eliminarlinkimg

from api.permissions import get_group_perms, require_model_perm
from api.views.generics import (
    PerPagePagination,
    clip_value_html,
    format_thousands,
    parse_order_by,
    register_simple_datatable,
)
from api.schemas.carga_schemas import (
    ReceptorOut, ReceptorCreate, ReceptorUpdate,
    AreaOut, AreaCreate, AreaUpdate,
    AseguradoraOut, AseguradoraCreate, AseguradoraUpdate,
    EmpresaOut, EmpresaCreate, EmpresaUpdate,
    ProgramaOut, ProgramaCreate, ProgramaUpdate,
    ProvinciaOut, ProvinciaCreate, ProvinciaUpdate,
    RegionOut, RegionCreate, RegionUpdate,
    DepartamentoCargaOut, DepartamentoCargaCreate, DepartamentoCargaUpdate,
    MunicipioOut, MunicipioCreate, MunicipioUpdate,
    LocalidadOut, LocalidadCreate, LocalidadUpdate,
    ObraOut, ObraCreate, ObraUpdate,
    PrototipoOut, PrototipoCreate, PrototipoUpdate,
    CertificadoRubroOut, CertificadoRubroCreate, CertificadoRubroUpdate,
    CertificadoFinanciamientoOut, CertificadoFinanciamientoCreate, CertificadoFinanciamientoUpdate,
    CertificadoOut, CertificadoCreate, CertificadoUpdate,
    ConjuntoLicitadoOut, ConjuntoLicitadoCreate, ConjuntoLicitadoUpdate,
    PlanDeTrabajosOut, PlanDeTrabajosCreate, PlanDeTrabajosUpdate,
    ContratoOut, ContratoCreate, ContratoUpdate,
    ContratoMontoOut, ContratoMontoCreate, ContratoMontoUpdate,
    ContratoRubroOut, ContratoRubroCreate, ContratoRubroUpdate,
    ContratosDigitalesOut, ContratosDigitalesCreate, ContratosDigitalesUpdate,
    ResolucionesDigitalesOut, ResolucionesDigitalesCreate, ResolucionesDigitalesUpdate,
    UviOut, UviCreate, UviUpdate,
    INDECOut, INDECCreate, INDECUpdate,
    PolizaOut, PolizaCreate, PolizaUpdate,
    PolizaMovimientoOut, PolizaMovimientoCreate, PolizaMovimientoUpdate,
)
from carga.models import (
    Area,
    Aseguradora,
    Certificado,
    CertificadoFinanciamiento,
    CertificadoRubro,
    ConjuntoLicitado,
    Contrato,
    ContratoMonto,
    ContratoRubro,
    ContratosDigitales,
    Departamento,
    Empresa,
    INDEC,
    Localidad,
    Municipio,
    Obra,
    obras_con_acumulado_anotado,
    PlanDeTrabajos,
    Poliza,
    Poliza_Movimiento,
    Programa,
    Prototipo,
    Provincia,
    Receptor,
    Region,
    ResolucionesDigitales,
    Uvi,
)

router = Router(tags=["carga"])


# --- Receptor ---
@router.get("/receptores/", response=List[ReceptorOut])
@decorate_view(require_model_perm(Receptor))
@paginate(PerPagePagination)
def list_receptores(request):
    return Receptor.objects.all().order_by("receptor_nombre")


@router.get("/receptor/{id}/", response=ReceptorOut)
@decorate_view(require_model_perm(Receptor))
def retrieve_receptor(request, id: int):
    return get_object_or_404(Receptor, id=id)


@router.post("/receptores/", response=ReceptorOut)
@decorate_view(require_model_perm(Receptor))
def create_receptor(request, payload: ReceptorCreate):
    return Receptor.objects.create(**payload.model_dump())


@router.put("/receptor/{id}/", response=ReceptorOut)
@decorate_view(require_model_perm(Receptor))
def update_receptor(request, id: int, payload: ReceptorUpdate):
    r = get_object_or_404(Receptor, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(r, field, value)
    r.save()
    return r


@router.delete("/receptor/{id}/")
@decorate_view(require_model_perm(Receptor))
def delete_receptor(request, id: int):
    deleted, _ = Receptor.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Area ---
@router.get("/areas/", response=List[AreaOut])
@decorate_view(require_model_perm(Area))
@paginate(PerPagePagination)
def list_areas(request):
    return Area.objects.all().order_by("area_nombre")


@router.get("/area/{id}/", response=AreaOut)
@decorate_view(require_model_perm(Area))
def retrieve_area(request, id: int):
    return get_object_or_404(Area, id=id)


@router.post("/areas/", response=AreaOut)
@decorate_view(require_model_perm(Area))
def create_area(request, payload: AreaCreate):
    return Area.objects.create(**payload.model_dump())


@router.put("/area/{id}/", response=AreaOut)
@decorate_view(require_model_perm(Area))
def update_area(request, id: int, payload: AreaUpdate):
    a = get_object_or_404(Area, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(a, field, value)
    a.save()
    return a


@router.delete("/area/{id}/")
@decorate_view(require_model_perm(Area))
def delete_area(request, id: int):
    deleted, _ = Area.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Aseguradora ---
@router.get("/aseguradoras/", response=List[AseguradoraOut])
@decorate_view(require_model_perm(Aseguradora))
@paginate(PerPagePagination)
def list_aseguradoras(request):
    return Aseguradora.objects.all().order_by("aseguradora_nombre")


@router.get("/aseguradora/{id}/", response=AseguradoraOut)
@decorate_view(require_model_perm(Aseguradora))
def retrieve_aseguradora(request, id: int):
    return get_object_or_404(Aseguradora, id=id)


@router.post("/aseguradoras/", response=AseguradoraOut)
@decorate_view(require_model_perm(Aseguradora))
def create_aseguradora(request, payload: AseguradoraCreate):
    return Aseguradora.objects.create(**payload.model_dump())


@router.put("/aseguradora/{id}/", response=AseguradoraOut)
@decorate_view(require_model_perm(Aseguradora))
def update_aseguradora(request, id: int, payload: AseguradoraUpdate):
    a = get_object_or_404(Aseguradora, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(a, field, value)
    a.save()
    return a


@router.delete("/aseguradora/{id}/")
@decorate_view(require_model_perm(Aseguradora))
def delete_aseguradora(request, id: int):
    deleted, _ = Aseguradora.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


def _aseguradora_datatable_row(a: Aseguradora, user) -> dict:
    id_ = str(a.id)
    editarlink = f"<a href='/obra/crear/aseguradora/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href='#'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/obra/eliminar/aseguradora/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("carga.delete_aseguradora"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("carga.change_aseguradora"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {"id": a.id, "aseguradora_nombre": a.aseguradora_nombre, "acciones": acciones}


register_simple_datatable(
    router, Aseguradora, "aseguradoras",
    order_fields={"id": "id", "aseguradora_nombre": "aseguradora_nombre"},
    filter_fields={"aseguradora_nombre": "aseguradora_nombre__icontains"},
    search_lookups=["aseguradora_nombre__icontains"],
    row_builder=_aseguradora_datatable_row,
    default_order="aseguradora_nombre",
)


# --- Empresa ---
@router.get("/empresas/", response=List[EmpresaOut])
@decorate_view(require_model_perm(Empresa))
@paginate(PerPagePagination)
def list_empresas(request, q: str = ""):
    qs = Empresa.objects.all().order_by("empresa_nombre")
    if q:
        qs = qs.filter(
            Q(empresa_nombre__icontains=q)
            | Q(empresa_cuit__icontains=q)
            | Q(empresa_titular_nombre__icontains=q)
        )
    return qs


@router.get("/empresa/{id}/", response=EmpresaOut)
@decorate_view(require_model_perm(Empresa))
def retrieve_empresa(request, id: int):
    return get_object_or_404(Empresa, id=id)


@router.post("/empresas/", response=EmpresaOut)
@decorate_view(require_model_perm(Empresa))
def create_empresa(request, payload: EmpresaCreate):
    return Empresa.objects.create(**payload.model_dump())


@router.put("/empresa/{id}/", response=EmpresaOut)
@decorate_view(require_model_perm(Empresa))
def update_empresa(request, id: int, payload: EmpresaUpdate):
    e = get_object_or_404(Empresa, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(e, field, value)
    e.save()
    return e


@router.delete("/empresa/{id}/")
@decorate_view(require_model_perm(Empresa))
def delete_empresa(request, id: int):
    deleted, _ = Empresa.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


def _empresa_datatable_row(e: Empresa, user) -> dict:
    id_ = str(e.id)
    editarlink = f"<a href='/obra/crear/empresa/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href='/obra/crear/empresa/obra/{id_}'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/obra/eliminar/empresa/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("carga.delete_empresa"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("carga.change_empresa"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {
        "id": e.id,
        "empresa_nombre": e.empresa_nombre,
        "empresa_cuit": e.empresa_cuit,
        "empresa_titular_nombre": e.empresa_titular_nombre,
        "empresa_direccion": e.empresa_direccion,
        "acciones": acciones,
    }


register_simple_datatable(
    router, Empresa, "empresas",
    order_fields={
        "id": "id", "empresa_nombre": "empresa_nombre", "empresa_cuit": "empresa_cuit",
        "empresa_titular_nombre": "empresa_titular_nombre", "empresa_direccion": "empresa_direccion",
    },
    filter_fields={
        "empresa_nombre": "empresa_nombre__icontains", "empresa_cuit": "empresa_cuit__icontains",
        "empresa_titular_nombre": "empresa_titular_nombre__icontains",
        "empresa_direccion": "empresa_direccion__icontains",
    },
    search_lookups=[
        "empresa_nombre__icontains", "empresa_cuit__icontains",
        "empresa_titular_nombre__icontains", "empresa_direccion__icontains",
    ],
    row_builder=_empresa_datatable_row,
)


# --- Programa ---
@router.get("/programas/", response=List[ProgramaOut])
@decorate_view(require_model_perm(Programa))
@paginate(PerPagePagination)
def list_programas(request):
    return Programa.objects.all().order_by("programa_nombre")


@router.get("/programa/{id}/", response=ProgramaOut)
@decorate_view(require_model_perm(Programa))
def retrieve_programa(request, id: int):
    return get_object_or_404(Programa, id=id)


@router.post("/programas/", response=ProgramaOut)
@decorate_view(require_model_perm(Programa))
def create_programa(request, payload: ProgramaCreate):
    return Programa.objects.create(**payload.model_dump())


@router.put("/programa/{id}/", response=ProgramaOut)
@decorate_view(require_model_perm(Programa))
def update_programa(request, id: int, payload: ProgramaUpdate):
    p = get_object_or_404(Programa, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(p, field, value)
    p.save()
    return p


@router.delete("/programa/{id}/")
@decorate_view(require_model_perm(Programa))
def delete_programa(request, id: int):
    deleted, _ = Programa.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


def _programa_datatable_row(p: Programa, user) -> dict:
    id_ = str(p.id)
    editarlink = f"<a href='/obra/crear/programa/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href='/obra/crear/programa/obra/{id_}'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/obra/eliminar/programa/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("carga.delete_programa"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("carga.change_programa"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {"id": p.id, "programa_nombre": p.programa_nombre, "acciones": acciones}


register_simple_datatable(
    router, Programa, "programas",
    order_fields={"id": "id", "programa_nombre": "programa_nombre"},
    filter_fields={"programa_nombre": "programa_nombre__icontains"},
    search_lookups=["programa_nombre__icontains"],
    row_builder=_programa_datatable_row,
)


# --- Provincia ---
@router.get("/provincias/", response=List[ProvinciaOut])
@decorate_view(require_model_perm(Provincia))
@paginate(PerPagePagination)
def list_provincias(request):
    return Provincia.objects.all().order_by("provincia_nombre")


@router.get("/provincia/{id}/", response=ProvinciaOut)
@decorate_view(require_model_perm(Provincia))
def retrieve_provincia(request, id: int):
    return get_object_or_404(Provincia, id=id)


@router.post("/provincias/", response=ProvinciaOut)
@decorate_view(require_model_perm(Provincia))
def create_provincia(request, payload: ProvinciaCreate):
    return Provincia.objects.create(**payload.model_dump())


@router.put("/provincia/{id}/", response=ProvinciaOut)
@decorate_view(require_model_perm(Provincia))
def update_provincia(request, id: int, payload: ProvinciaUpdate):
    p = get_object_or_404(Provincia, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(p, field, value)
    p.save()
    return p


@router.delete("/provincia/{id}/")
@decorate_view(require_model_perm(Provincia))
def delete_provincia(request, id: int):
    deleted, _ = Provincia.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Region ---
@router.get("/regiones/", response=List[RegionOut])
@decorate_view(require_model_perm(Region))
@paginate(PerPagePagination)
def list_regiones(request):
    return Region.objects.all().order_by("id")


@router.get("/region/{id}/", response=RegionOut)
@decorate_view(require_model_perm(Region))
def retrieve_region(request, id: int):
    return get_object_or_404(Region, id=id)


@router.post("/regiones/", response=RegionOut)
@decorate_view(require_model_perm(Region))
def create_region(request, payload: RegionCreate):
    return Region.objects.create(**payload.model_dump())


@router.put("/region/{id}/", response=RegionOut)
@decorate_view(require_model_perm(Region))
def update_region(request, id: int, payload: RegionUpdate):
    r = get_object_or_404(Region, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(r, field, value)
    r.save()
    return r


@router.delete("/region/{id}/")
@decorate_view(require_model_perm(Region))
def delete_region(request, id: int):
    deleted, _ = Region.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


def _region_datatable_row(r: Region, user) -> dict:
    id_ = str(r.id)
    editarlink = f"<a href='/obra/crear/region/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href='/obra/crear/region/obra/{id_}'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/obra/eliminar/region/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("carga.delete_region"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("carga.change_region"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {"id": r.id, "region_numero": r.region_numero, "acciones": acciones}


register_simple_datatable(
    router, Region, "regiones",
    order_fields={"region_numero": "region_numero"},
    filter_fields={"region_numero": "region_numero__icontains"},
    search_lookups=["region_numero__icontains"],
    row_builder=_region_datatable_row,
    default_order="region_numero",
)


# --- Departamento (carga) ---
@router.get("/departamentos-carga/", response=List[DepartamentoCargaOut])
@decorate_view(require_model_perm(Departamento))
@paginate(PerPagePagination)
def list_departamentos_carga(request):
    return Departamento.objects.all().order_by("departamento_nombre")


@router.get("/departamento-carga/{id}/", response=DepartamentoCargaOut)
@decorate_view(require_model_perm(Departamento))
def retrieve_departamento_carga(request, id: int):
    return get_object_or_404(Departamento, id=id)


@router.post("/departamentos-carga/", response=DepartamentoCargaOut)
@decorate_view(require_model_perm(Departamento))
def create_departamento_carga(request, payload: DepartamentoCargaCreate):
    return Departamento.objects.create(**payload.model_dump())


@router.put("/departamento-carga/{id}/", response=DepartamentoCargaOut)
@decorate_view(require_model_perm(Departamento))
def update_departamento_carga(request, id: int, payload: DepartamentoCargaUpdate):
    d = get_object_or_404(Departamento, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(d, field, value)
    d.save()
    return d


@router.delete("/departamento-carga/{id}/")
@decorate_view(require_model_perm(Departamento))
def delete_departamento_carga(request, id: int):
    deleted, _ = Departamento.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


def _departamento_carga_datatable_row(d: Departamento, user) -> dict:
    id_ = str(d.id)
    editarlink = f"<a href='/obra/crear/departamento/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href='/obra/crear/departamento/{id_}'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/obra/eliminar/departamento/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("carga.delete_departamento"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("carga.change_departamento"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {"id": d.id, "departamento_nombre": d.departamento_nombre, "acciones": acciones}


register_simple_datatable(
    router, Departamento, "departamentos-carga",
    order_fields={"id": "id", "departamento_nombre": "departamento_nombre"},
    filter_fields={"departamento_nombre": "departamento_nombre__icontains"},
    search_lookups=["departamento_nombre__icontains"],
    row_builder=_departamento_carga_datatable_row,
)


# --- Municipio ---
@router.get("/municipios/", response=List[MunicipioOut])
@decorate_view(require_model_perm(Municipio))
@paginate(PerPagePagination)
def list_municipios(request, departamento: str = ""):
    qs = Municipio.objects.all().order_by("municipio_nombre")
    if departamento:
        qs = qs.filter(municipio_departamento_id=departamento)
    return qs


@router.get("/municipio/{id}/", response=MunicipioOut)
@decorate_view(require_model_perm(Municipio))
def retrieve_municipio(request, id: int):
    return get_object_or_404(Municipio, id=id)


@router.post("/municipios/", response=MunicipioOut)
@decorate_view(require_model_perm(Municipio))
def create_municipio(request, payload: MunicipioCreate):
    return Municipio.objects.create(**payload.model_dump())


@router.put("/municipio/{id}/", response=MunicipioOut)
@decorate_view(require_model_perm(Municipio))
def update_municipio(request, id: int, payload: MunicipioUpdate):
    m = get_object_or_404(Municipio, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(m, field, value)
    m.save()
    return m


@router.delete("/municipio/{id}/")
@decorate_view(require_model_perm(Municipio))
def delete_municipio(request, id: int):
    deleted, _ = Municipio.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


def _municipio_datatable_row(m: Municipio, user) -> dict:
    id_ = str(m.id)
    editarlink = f"<a href='/obra/crear/municipio/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href='/obra/crear/municipio/obra/{id_}'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/obra/eliminar/municipio/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("carga.delete_municipio"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("carga.change_municipio"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {
        "id": m.id,
        "municipio_nombre": m.municipio_nombre,
        "municipio_departamento": m.municipio_departamento.departamento_nombre,
        "municipio_region": m.municipio_region.region_numero if m.municipio_region_id else "",
        "acciones": acciones,
    }


register_simple_datatable(
    router, Municipio, "municipios",
    order_fields={
        "id": "id",
        "municipio_nombre": "municipio_nombre",
        "municipio_departamento": "municipio_departamento__departamento_nombre",
        "municipio_region": "municipio_region__region_numero",
    },
    filter_fields={
        "municipio_nombre": "municipio_nombre__icontains",
        "municipio_departamento": "municipio_departamento__departamento_nombre__icontains",
        "municipio_region": "municipio_region__region_numero__icontains",
    },
    search_lookups=[
        "municipio_nombre__icontains",
        "municipio_departamento__departamento_nombre__icontains",
        "municipio_region__region_numero__icontains",
    ],
    row_builder=_municipio_datatable_row,
    queryset=Municipio.objects.select_related("municipio_departamento", "municipio_region"),
)


# --- Localidad ---
@router.get("/localidades/", response=List[LocalidadOut])
@decorate_view(require_model_perm(Localidad))
@paginate(PerPagePagination)
def list_localidades(request, departamento: str = ""):
    qs = Localidad.objects.all().order_by("localidad_nombre")
    if departamento:
        qs = qs.filter(localidad_departamento_id=departamento)
    return qs


@router.get("/localidad/{id}/", response=LocalidadOut)
@decorate_view(require_model_perm(Localidad))
def retrieve_localidad(request, id: int):
    return get_object_or_404(Localidad, id=id)


@router.post("/localidades/", response=LocalidadOut)
@decorate_view(require_model_perm(Localidad))
def create_localidad(request, payload: LocalidadCreate):
    return Localidad.objects.create(**payload.model_dump())


@router.put("/localidad/{id}/", response=LocalidadOut)
@decorate_view(require_model_perm(Localidad))
def update_localidad(request, id: int, payload: LocalidadUpdate):
    l = get_object_or_404(Localidad, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(l, field, value)
    l.save()
    return l


@router.delete("/localidad/{id}/")
@decorate_view(require_model_perm(Localidad))
def delete_localidad(request, id: int):
    deleted, _ = Localidad.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


def _localidad_datatable_row(l: Localidad, user) -> dict:
    id_ = str(l.id)
    editarlink = f"<a href='/obra/crear/localidad/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href='/obra/crear/localidad/obra/{id_}'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/obra/eliminar/localidad/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("carga.delete_localidad"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("carga.change_localidad"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {
        "id": l.id,
        "localidad_nombre": l.localidad_nombre,
        "localidad_municipio": l.localidad_municipio.municipio_nombre,
        "localidad_departamento": l.localidad_departamento.departamento_nombre,
        "localidad_funcion": l.localidad_funcion or "",
        "acciones": acciones,
    }


register_simple_datatable(
    router, Localidad, "localidades",
    order_fields={
        "id": "id",
        "localidad_nombre": "localidad_nombre",
        "localidad_municipio": "localidad_municipio__municipio_nombre",
        "localidad_departamento": "localidad_departamento__departamento_nombre",
        "localidad_funcion": "localidad_funcion",
    },
    filter_fields={
        "localidad_nombre": "localidad_nombre__icontains",
        "localidad_municipio": "localidad_municipio__municipio_nombre__icontains",
        "localidad_departamento": "localidad_departamento__departamento_nombre__icontains",
        "localidad_funcion": "localidad_funcion",
    },
    search_lookups=[
        "localidad_nombre__icontains",
        "localidad_municipio__municipio_nombre__icontains",
        "localidad_departamento__departamento_nombre__icontains",
    ],
    row_builder=_localidad_datatable_row,
    default_order="localidad_nombre",
    queryset=Localidad.objects.select_related("localidad_municipio", "localidad_departamento"),
)


@router.get("/datatables/localidades/filtro-funcion/")
@decorate_view(require_model_perm(Localidad))
def datatable_localidades_filtro_funcion(request):
    valores = (
        Localidad.objects.exclude(localidad_funcion=None)
        .exclude(localidad_funcion="")
        .values_list("localidad_funcion", flat=True)
        .distinct()
        .order_by("localidad_funcion")
    )
    return {"choices": [[v, v] for v in valores]}


# --- Obra (complex model with M2M fields) ---
@router.get("/obras/", response=List[ObraOut])
@decorate_view(require_model_perm(Obra))
@paginate(PerPagePagination)
def list_obras(request, empresa: str = "", programa: str = "", region: str = "", q: str = ""):
    qs = Obra.objects.select_related("obra_empresa", "obra_programa").all().order_by("-id")
    if empresa:
        qs = qs.filter(obra_empresa_id=empresa)
    if programa:
        qs = qs.filter(obra_programa_id=programa)
    if region:
        qs = qs.filter(obra_region_id=region)
    if q:
        qs = qs.filter(
            Q(obra_nombre__icontains=q)
            | Q(obra_expediente__icontains=q)
            | Q(obra_resolucion__icontains=q)
        )
    return qs


def _obra_out(o: Obra) -> dict:
    return {
        "id": o.id,
        "obra_uuid": str(o.obra_uuid),
        "obra_nombre": o.obra_nombre,
        "obra_soluciones": o.obra_soluciones,
        "obra_empresa_id": o.obra_empresa_id,
        "obra_region_id": o.obra_region_id,
        "departamento_ids": list(o.obra_departamento_m.values_list("id", flat=True)),
        "municipio_ids": list(o.obra_municipio_m.values_list("id", flat=True)),
        "localidad_ids": list(o.obra_localidad_m.values_list("id", flat=True)),
        "obra_conjunto_id": o.obra_conjunto_id,
        "obra_grupo": o.obra_grupo,
        "obra_plazo": o.obra_plazo,
        "obra_programa_id": o.obra_programa_id,
        "obra_convenio": o.obra_convenio,
        "obra_expediente": o.obra_expediente,
        "obra_resolucion": o.obra_resolucion,
        "obra_licitacion_tipo": o.obra_licitacion_tipo,
        "obra_licitacion_numero": o.obra_licitacion_numero,
        "obra_licitacion_ano": o.obra_licitacion_ano,
        "obra_nomenclatura": o.obra_nomenclatura,
        "obra_nomenclatura_plano": o.obra_nomenclatura_plano,
        "obra_fecha_entrega": o.obra_fecha_entrega,
        "obra_fecha_contrato": o.obra_fecha_contrato,
        "obra_expediente_costo": o.obra_expediente_costo,
        "inspector_ids": list(o.obra_inspector.values_list("id", flat=True)),
        "obra_observaciones": o.obra_observaciones,
        "obra_contrato_nacion_pesos": o.obra_contrato_nacion_pesos,
        "obra_contrato_nacion_uvi": o.obra_contrato_nacion_uvi,
        "obra_contrato_provincia_pesos": o.obra_contrato_provincia_pesos,
        "obra_contrato_provincia_uvi": o.obra_contrato_provincia_uvi,
        "obra_contrato_total_pesos": o.obra_contrato_total_pesos,
    }


@router.get("/obra/{id}/", response=ObraOut)
@decorate_view(require_model_perm(Obra))
def retrieve_obra(request, id: int):
    o = get_object_or_404(
        Obra.objects.select_related("obra_empresa", "obra_region", "obra_programa", "obra_conjunto"),
        id=id,
    )
    return _obra_out(o)


@router.post("/obras/", response=ObraOut)
@decorate_view(require_model_perm(Obra))
def create_obra(request, payload: ObraCreate):
    data = payload.model_dump()
    m2m = {
        "departamento_ids": "obra_departamento_m",
        "municipio_ids": "obra_municipio_m",
        "localidad_ids": "obra_localidad_m",
        "inspector_ids": "obra_inspector",
    }
    m2m_values = {k: data.pop(k) for k in list(m2m)}
    o = Obra.objects.create(**data)
    for payload_key, attname in m2m.items():
        ids = m2m_values.get(payload_key) or []
        if ids:
            getattr(o, attname).set(ids)
    return _obra_out(o)


@router.put("/obra/{id}/", response=ObraOut)
@decorate_view(require_model_perm(Obra))
def update_obra(request, id: int, payload: ObraUpdate):
    o = get_object_or_404(Obra, id=id)
    data = payload.model_dump(exclude_unset=True)
    m2m = {
        "departamento_ids": "obra_departamento_m",
        "municipio_ids": "obra_municipio_m",
        "localidad_ids": "obra_localidad_m",
        "inspector_ids": "obra_inspector",
    }
    for payload_key, attname in list(m2m.items()):
        if payload_key in data:
            getattr(o, attname).set(data.pop(payload_key))
    for field, value in data.items():
        setattr(o, field, value)
    o.save()
    return _obra_out(o)


@router.delete("/obra/{id}/")
@decorate_view(require_model_perm(Obra))
def delete_obra(request, id: int):
    deleted, _ = Obra.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Obra datatable (server-side data for the DataTables listing) ---

_OBRA_DATATABLE_ORDER_FIELDS = {
    "id": "id",
    "obra_programa": "obra_programa__programa_nombre",
    "obra_convenio": "obra_convenio",
    "obra_nombre": "obra_nombre",
    "obra_empresa": "obra_empresa__empresa_nombre",
}

_OBRA_DATATABLE_FILTER_FIELDS = {
    "id": "id__icontains",
    "obra_programa": "obra_programa__programa_nombre__icontains",
    "obra_convenio": "obra_convenio__icontains",
    "obra_nombre": "obra_nombre__icontains",
    "obra_empresa": "obra_empresa__empresa_nombre__icontains",
    "obra_localidad": "obra_localidad_m__localidad_nombre__icontains",
}


def _obra_datatable_row(o: Obra, user) -> dict:
    acumulado = getattr(o, "obra_acum_pct_anotado", None)
    anticipo_acumulado = getattr(o, "obra_anticipo_acumulado_anotado", None)

    editarlink = f"<a href='/obra/crear/obra/{o.id}'>{editlinkimg}</a>"
    detallelink = f"<a href='/obra/crear/obra/estado/{o.id}'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/obra/eliminar/obra/{o.id}'>{eliminarlinkimg}</a>"
    if user.has_perm("carga.delete_obra"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("carga.change_obra"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink

    return {
        "id": o.id,
        "obra_programa": o.obra_programa.programa_nombre,
        "obra_convenio": o.obra_convenio,
        "obra_nombre": o.obra_nombre,
        "obra_empresa": o.obra_empresa.empresa_nombre,
        "obra_localidad": ", ".join(l.localidad_nombre for l in o.obra_localidad_m.all()),
        "obra_acumulado": (str(acumulado) if acumulado is not None else "0.00") + "%",
        "obra_anticipo_acumulado": (str(anticipo_acumulado) if anticipo_acumulado is not None else "0.00") + "%",
        "acciones": acciones,
    }


@router.get("/datatables/obras/")
@decorate_view(require_model_perm(Obra))
def datatable_obras(
    request,
    draw: int = 1,
    start: int = 0,
    length: int = 50,
    search: str = "",
    order_by: str = "-id",
    filters: str = "{}",
):
    qs = obras_con_acumulado_anotado(
        Obra.objects.select_related("obra_empresa", "obra_programa").prefetch_related("obra_localidad_m")
    )
    records_total = qs.count()

    try:
        active_filters = json.loads(filters)
    except (TypeError, ValueError):
        active_filters = {}
    needs_distinct = False
    for key, value in active_filters.items():
        lookup = _OBRA_DATATABLE_FILTER_FIELDS.get(key)
        if lookup and value not in (None, ""):
            qs = qs.filter(**{lookup: value})
            if key == "obra_localidad":
                needs_distinct = True
    if needs_distinct:
        qs = qs.distinct()

    if search:
        qs = qs.filter(
            Q(id__icontains=search)
            | Q(obra_programa__programa_nombre__icontains=search)
            | Q(obra_convenio__icontains=search)
            | Q(obra_nombre__icontains=search)
            | Q(obra_empresa__empresa_nombre__icontains=search)
            | Q(obra_localidad_m__localidad_nombre__icontains=search)
        ).distinct()

    records_filtered = qs.count()

    qs = qs.order_by(*parse_order_by(order_by, _OBRA_DATATABLE_ORDER_FIELDS), "id")

    page = qs[start:] if length == -1 else qs[start:start + length]

    return {
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": [_obra_datatable_row(o, request.user) for o in page],
    }


@router.get("/datatables/obras/{id}/detalle/")
@decorate_view(require_model_perm(Obra))
def datatable_obras_detalle(request, id: int):
    o = get_object_or_404(
        Obra.objects.select_related("obra_empresa", "obra_programa").prefetch_related("obra_madre"),
        id=id,
    )
    html = render_to_string(
        "ajax_datatable/carga/obra/render_row_details.html",
        {"model": Obra, "object": o},
        request=request,
    )
    return {"html": html}


# --- Obra extendida datatable (full export-style listing, ~35 columns) ---

_OBRA_EXT_ORDER_FIELDS = {
    "id": "id",
    "obra_nombre": "obra_nombre",
    "obra_soluciones": "obra_soluciones",
    "obra_empresa": "obra_empresa__empresa_nombre",
    "obra_region": "obra_region__region_numero",
    "obra_conjunto": "obra_conjunto__conjunto_nombre",
    "obra_grupo": "obra_grupo",
    "obra_plazo": "obra_plazo",
    "obra_programa": "obra_programa__programa_nombre",
    "obra_convenio": "obra_convenio",
    "obra_expediente": "obra_expediente",
    "obra_resolucion": "obra_resolucion",
    "obra_licitacion_tipo": "obra_licitacion_tipo",
    "obra_licitacion_numero": "obra_licitacion_numero",
    "obra_licitacion_ano": "obra_licitacion_ano",
    "obra_nomenclatura": "obra_nomenclatura",
    "obra_nomenclatura_plano": "obra_nomenclatura_plano",
    "obra_fecha_entrega": "obra_fecha_entrega",
    "obra_fecha_contrato": "obra_fecha_contrato",
    "obra_observaciones": "obra_observaciones",
    "obra_contrato_nacion_pesos": "obra_contrato_nacion_pesos",
    "obra_contrato_nacion_uvi": "obra_contrato_nacion_uvi",
    "obra_contrato_nacion_uvi_fecha": "obra_contrato_nacion_uvi_fecha",
    "obra_contrato_provincia_pesos": "obra_contrato_provincia_pesos",
    "obra_contrato_provincia_uvi": "obra_contrato_provincia_uvi",
    "obra_contrato_provincia_uvi_fecha": "obra_contrato_provincia_uvi_fecha",
    "obra_contrato_terceros_pesos": "obra_contrato_terceros_pesos",
    "obra_contrato_terceros_uvi": "obra_contrato_terceros_uvi",
    "obra_contrato_terceros_uvi_fecha": "obra_contrato_terceros_uvi_fecha",
}

_OBRA_EXT_FILTER_FIELDS = {
    "id": "id__icontains",
    "obra_nombre": "obra_nombre__icontains",
    "obra_soluciones": "obra_soluciones__icontains",
    "obra_empresa": "obra_empresa__empresa_nombre__icontains",
    "obra_region": "obra_region__region_numero__icontains",
    "obra_departamento_m": "obra_departamento_m__departamento_nombre__icontains",
    "obra_municipio_m": "obra_municipio_m__municipio_nombre__icontains",
    "obra_localidad_m": "obra_localidad_m__localidad_nombre__icontains",
    "obra_conjunto": "obra_conjunto__conjunto_nombre__icontains",
    "obra_grupo": "obra_grupo__icontains",
    "obra_plazo": "obra_plazo__icontains",
    "obra_programa": "obra_programa_id",
    "obra_convenio": "obra_convenio__icontains",
    "obra_expediente": "obra_expediente__icontains",
    "obra_resolucion": "obra_resolucion__icontains",
    "obra_licitacion_tipo": "obra_licitacion_tipo",
    "obra_licitacion_numero": "obra_licitacion_numero__icontains",
    "obra_licitacion_ano": "obra_licitacion_ano",
    "obra_nomenclatura": "obra_nomenclatura__icontains",
    "obra_nomenclatura_plano": "obra_nomenclatura_plano__icontains",
    "obra_fecha_entrega": "obra_fecha_entrega",
    "obra_fecha_contrato": "obra_fecha_contrato",
    "obra_observaciones": "obra_observaciones__icontains",
    "obra_principal": "obra_principal__obra_nombre__icontains",
    "obra_contrato_nacion_pesos": "obra_contrato_nacion_pesos__icontains",
    "obra_contrato_nacion_uvi": "obra_contrato_nacion_uvi__icontains",
    "obra_contrato_nacion_uvi_fecha": "obra_contrato_nacion_uvi_fecha",
    "obra_contrato_provincia_pesos": "obra_contrato_provincia_pesos__icontains",
    "obra_contrato_provincia_uvi": "obra_contrato_provincia_uvi__icontains",
    "obra_contrato_provincia_uvi_fecha": "obra_contrato_provincia_uvi_fecha",
    "obra_contrato_terceros_pesos": "obra_contrato_terceros_pesos__icontains",
    "obra_contrato_terceros_uvi": "obra_contrato_terceros_uvi__icontains",
    "obra_contrato_terceros_uvi_fecha": "obra_contrato_terceros_uvi_fecha",
}

_OBRA_EXT_DISTINCT_FILTER_KEYS = {"obra_departamento_m", "obra_municipio_m", "obra_localidad_m", "obra_principal"}

_OBRA_EXT_SEARCH_LOOKUPS = [
    "obra_nombre__icontains", "obra_empresa__empresa_nombre__icontains",
    "obra_region__region_numero__icontains", "obra_departamento_m__departamento_nombre__icontains",
    "obra_municipio_m__municipio_nombre__icontains", "obra_localidad_m__localidad_nombre__icontains",
    "obra_conjunto__conjunto_nombre__icontains", "obra_grupo__icontains", "obra_plazo__icontains",
    "obra_programa__programa_nombre__icontains", "obra_convenio__icontains", "obra_expediente__icontains",
    "obra_resolucion__icontains", "obra_nomenclatura__icontains", "obra_nomenclatura_plano__icontains",
    "obra_observaciones__icontains", "obra_principal__obra_nombre__icontains",
]


def _obra_ext_datatable_row(o: Obra, user) -> dict:
    acumulado = getattr(o, "obra_acum_pct_anotado", None)
    anticipo_acumulado = getattr(o, "obra_anticipo_acumulado_anotado", None)

    id_ = str(o.id)
    detallelink = f"<a href='/obra/crear/obra/estado/{id_}'>{detallelinkimg}</a>"
    if user.has_perm("carga.change_obra"):
        editarlink = f"<a href='/obra/crear/obra/{id_}'>{editlinkimg}</a>"
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink

    return {
        "id": o.id,
        "obra_nombre": clip_value_html(o.obra_nombre, 100),
        "obra_soluciones": o.obra_soluciones,
        "obra_empresa": o.obra_empresa.empresa_nombre,
        "obra_region": o.obra_region.region_numero if o.obra_region_id else "",
        "obra_departamento_m": ", ".join(d.departamento_nombre for d in o.obra_departamento_m.all()),
        "obra_municipio_m": ", ".join(m.municipio_nombre for m in o.obra_municipio_m.all()),
        "obra_localidad_m": ", ".join(l.localidad_nombre for l in o.obra_localidad_m.all()),
        "obra_conjunto": clip_value_html(o.obra_conjunto.conjunto_nombre, 100) if o.obra_conjunto_id else "",
        "obra_grupo": o.obra_grupo or "",
        "obra_plazo": o.obra_plazo or "",
        "obra_programa": clip_value_html(o.obra_programa.programa_nombre, 100),
        "obra_convenio": o.obra_convenio or "",
        "obra_expediente": o.obra_expediente,
        "obra_resolucion": o.obra_resolucion or "",
        "obra_licitacion_tipo": o.get_obra_licitacion_tipo_display() if o.obra_licitacion_tipo else "",
        "obra_licitacion_numero": o.obra_licitacion_numero,
        "obra_licitacion_ano": o.obra_licitacion_ano,
        "obra_nomenclatura": clip_value_html(o.obra_nomenclatura or "", 100),
        "obra_nomenclatura_plano": o.obra_nomenclatura_plano or "",
        "obra_fecha_entrega": o.obra_fecha_entrega.isoformat() if o.obra_fecha_entrega else "",
        "obra_fecha_contrato": o.obra_fecha_contrato.isoformat() if o.obra_fecha_contrato else "",
        "obra_inspector": ", ".join(str(agente) for agente in o.obra_inspector.all()),
        "obra_observaciones": clip_value_html(o.obra_observaciones or "", 100),
        "obra_contrato_nacion_pesos": format_thousands(o.obra_contrato_nacion_pesos),
        "obra_contrato_nacion_uvi": format_thousands(o.obra_contrato_nacion_uvi),
        "obra_contrato_nacion_uvi_fecha": o.obra_contrato_nacion_uvi_fecha.isoformat() if o.obra_contrato_nacion_uvi_fecha else "",
        "obra_contrato_provincia_pesos": format_thousands(o.obra_contrato_provincia_pesos),
        "obra_contrato_provincia_uvi": format_thousands(o.obra_contrato_provincia_uvi),
        "obra_contrato_provincia_uvi_fecha": o.obra_contrato_provincia_uvi_fecha.isoformat() if o.obra_contrato_provincia_uvi_fecha else "",
        "obra_contrato_terceros_pesos": format_thousands(o.obra_contrato_terceros_pesos),
        "obra_contrato_terceros_uvi": format_thousands(o.obra_contrato_terceros_uvi),
        "obra_contrato_terceros_uvi_fecha": o.obra_contrato_terceros_uvi_fecha.isoformat() if o.obra_contrato_terceros_uvi_fecha else "",
        "obra_principal": ", ".join(m.obra_nombre for m in o.obra_principal.all()),
        "obra_acumulado": (str(acumulado) if acumulado is not None else "0.00") + "%",
        "obra_anticipo_acumulado": (str(anticipo_acumulado) if anticipo_acumulado is not None else "0.00") + "%",
        "acciones": acciones,
    }


@router.get("/datatables/obras-extendida/")
@decorate_view(require_model_perm(Obra))
def datatable_obras_extendida(
    request,
    draw: int = 1,
    start: int = 0,
    length: int = 50,
    search: str = "",
    order_by: str = "-id",
    filters: str = "{}",
):
    qs = obras_con_acumulado_anotado(
        Obra.objects.select_related("obra_empresa", "obra_region", "obra_conjunto", "obra_programa")
        .prefetch_related(
            "obra_departamento_m", "obra_municipio_m", "obra_localidad_m", "obra_inspector", "obra_principal",
        )
    )
    records_total = qs.count()

    try:
        active_filters = json.loads(filters)
    except (TypeError, ValueError):
        active_filters = {}
    needs_distinct = False
    for key, value in active_filters.items():
        lookup = _OBRA_EXT_FILTER_FIELDS.get(key)
        if not lookup or value in (None, ""):
            continue
        qs = qs.filter(**{lookup: value})
        if key in _OBRA_EXT_DISTINCT_FILTER_KEYS:
            needs_distinct = True
    if needs_distinct:
        qs = qs.distinct()

    if search:
        search_q = Q()
        for lookup in _OBRA_EXT_SEARCH_LOOKUPS:
            search_q |= Q(**{lookup: search})
        qs = qs.filter(search_q).distinct()

    records_filtered = qs.count()
    qs = qs.order_by(*parse_order_by(order_by, _OBRA_EXT_ORDER_FIELDS), "id")
    page = qs[start:] if length == -1 else qs[start:start + length]

    return {
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": [_obra_ext_datatable_row(o, request.user) for o in page],
    }


@router.get("/datatables/obras-extendida/filtro-programa/")
@decorate_view(require_model_perm(Obra))
def datatable_obras_extendida_filtro_programa(request):
    choices = (
        Obra.objects.exclude(obra_programa=None)
        .values_list("obra_programa_id", "obra_programa__programa_nombre")
        .distinct()
        .order_by("obra_programa__programa_nombre")
    )
    return {"choices": list(choices)}


@router.get("/datatables/obras-extendida/filtro-ano/")
@decorate_view(require_model_perm(Obra))
def datatable_obras_extendida_filtro_ano(request):
    valores = (
        Obra.objects.exclude(obra_licitacion_ano=None)
        .values_list("obra_licitacion_ano", flat=True)
        .distinct()
        .order_by("obra_licitacion_ano")
    )
    return {"choices": [[str(v), str(v)] for v in valores]}


# --- Prototipo ---
@router.get("/prototipos/", response=List[PrototipoOut])
@decorate_view(require_model_perm(Prototipo))
@paginate(PerPagePagination)
def list_prototipos(request, obra: str = ""):
    qs = Prototipo.objects.select_related("prototipo_obra").all().order_by("-id")
    if obra:
        qs = qs.filter(prototipo_obra_id=obra)
    return qs


@router.get("/prototipo/{id}/", response=PrototipoOut)
@decorate_view(require_model_perm(Prototipo))
def retrieve_prototipo(request, id: int):
    return get_object_or_404(Prototipo, id=id)


@router.post("/prototipos/", response=PrototipoOut)
@decorate_view(require_model_perm(Prototipo))
def create_prototipo(request, payload: PrototipoCreate):
    return Prototipo.objects.create(**payload.model_dump())


@router.put("/prototipo/{id}/", response=PrototipoOut)
@decorate_view(require_model_perm(Prototipo))
def update_prototipo(request, id: int, payload: PrototipoUpdate):
    p = get_object_or_404(Prototipo, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(p, field, value)
    p.save()
    return p


@router.delete("/prototipo/{id}/")
@decorate_view(require_model_perm(Prototipo))
def delete_prototipo(request, id: int):
    deleted, _ = Prototipo.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- CertificadoRubro ---
@router.get("/rubros/", response=List[CertificadoRubroOut])
@decorate_view(require_model_perm(CertificadoRubro))
@paginate(PerPagePagination)
def list_rubros(request):
    return CertificadoRubro.objects.all().order_by("certificadorubro_nombre")


@router.get("/rubro/{id}/", response=CertificadoRubroOut)
@decorate_view(require_model_perm(CertificadoRubro))
def retrieve_rubro(request, id: int):
    return get_object_or_404(CertificadoRubro, id=id)


@router.post("/rubros/", response=CertificadoRubroOut)
@decorate_view(require_model_perm(CertificadoRubro))
def create_rubro(request, payload: CertificadoRubroCreate):
    return CertificadoRubro.objects.create(**payload.model_dump())


@router.put("/rubro/{id}/", response=CertificadoRubroOut)
@decorate_view(require_model_perm(CertificadoRubro))
def update_rubro(request, id: int, payload: CertificadoRubroUpdate):
    r = get_object_or_404(CertificadoRubro, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(r, field, value)
    r.save()
    return r


@router.delete("/rubro/{id}/")
@decorate_view(require_model_perm(CertificadoRubro))
def delete_rubro(request, id: int):
    deleted, _ = CertificadoRubro.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- CertificadoFinanciamiento ---
@router.get("/financiamientos/", response=List[CertificadoFinanciamientoOut])
@decorate_view(require_model_perm(CertificadoFinanciamiento))
@paginate(PerPagePagination)
def list_financiamientos(request):
    return CertificadoFinanciamiento.objects.all().order_by("certificadofinanciamiento_nombre")


@router.get("/financiamiento/{id}/", response=CertificadoFinanciamientoOut)
@decorate_view(require_model_perm(CertificadoFinanciamiento))
def retrieve_financiamiento(request, id: int):
    return get_object_or_404(CertificadoFinanciamiento, id=id)


@router.post("/financiamientos/", response=CertificadoFinanciamientoOut)
@decorate_view(require_model_perm(CertificadoFinanciamiento))
def create_financiamiento(request, payload: CertificadoFinanciamientoCreate):
    return CertificadoFinanciamiento.objects.create(**payload.model_dump())


@router.put("/financiamiento/{id}/", response=CertificadoFinanciamientoOut)
@decorate_view(require_model_perm(CertificadoFinanciamiento))
def update_financiamiento(request, id: int, payload: CertificadoFinanciamientoUpdate):
    f = get_object_or_404(CertificadoFinanciamiento, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(f, field, value)
    f.save()
    return f


@router.delete("/financiamiento/{id}/")
@decorate_view(require_model_perm(CertificadoFinanciamiento))
def delete_financiamiento(request, id: int):
    deleted, _ = CertificadoFinanciamiento.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Certificado ---
@router.get("/certificados/", response=List[CertificadoOut])
@decorate_view(require_model_perm(Certificado), get_group_perms("gciaoperativa_usuarios"))
@paginate(PerPagePagination)
def list_certificados(request, obra: str = ""):
    qs = Certificado.objects.select_related("certificado_obra").all().order_by("-certificado_fecha")
    if obra:
        qs = qs.filter(certificado_obra_id=obra)
    return qs


@router.get("/certificado/{id}/", response=CertificadoOut)
@decorate_view(require_model_perm(Certificado))
def retrieve_certificado(request, id: int):
    return get_object_or_404(Certificado, id=id)


@router.post("/certificados/", response=CertificadoOut)
@decorate_view(require_model_perm(Certificado))
def create_certificado(request, payload: CertificadoCreate):
    return Certificado.objects.create(**payload.model_dump())


@router.put("/certificado/{id}/", response=CertificadoOut)
@decorate_view(require_model_perm(Certificado))
def update_certificado(request, id: int, payload: CertificadoUpdate):
    c = get_object_or_404(Certificado, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(c, field, value)
    c.save()
    return c


@router.delete("/certificado/{id}/")
@decorate_view(require_model_perm(Certificado))
def delete_certificado(request, id: int):
    deleted, _ = Certificado.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


_CERTIFICADO_DATATABLE_ORDER_FIELDS = {
    "id": "id",
    "certificado_obra": "certificado_obra__obra_nombre",
    "certificado_empresa": "certificado_obra__obra_empresa__empresa_nombre",
    "certificado_expediente": "certificado_expediente",
    "certificado_fecha": "certificado_fecha",
    "certificado_financiamiento": "certificado_financiamiento",
    "certificado_rubro_db": "certificado_rubro_db__certificadorubro_nombre",
    "certificado_rubro_anticipo": "certificado_rubro_anticipo",
    "certificado_rubro_obra": "certificado_rubro_obra",
    "certificado_rubro_devanticipo": "certificado_rubro_devanticipo",
    "certificado_monto_cobrar": "certificado_monto_cobrar",
    "certificado_monto_cobrar_uvi": "certificado_monto_cobrar_uvi",
    "certificado_mes_pct": "certificado_mes_pct",
}

_CERTIFICADO_DATATABLE_FILTER_FIELDS = {
    "certificado_obra": "certificado_obra__obra_nombre__icontains",
    "certificado_empresa": "certificado_obra__obra_empresa__empresa_nombre__icontains",
    "certificado_expediente": "certificado_expediente__icontains",
    "certificado_fecha": "certificado_fecha",
    "certificado_financiamiento": "certificado_financiamiento",
    "certificado_rubro_db": "certificado_rubro_db_id",
}


def _certificado_datatable_row(c: Certificado, user) -> dict:
    id_ = str(c.id)
    editarlink = f"<a href='/obra/crear/certificado/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href='/obra/crear/certificado/detalle/{id_}'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/obra/eliminar/certificado/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("carga.delete_certificado"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("carga.change_certificado"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {
        "id": c.id,
        "certificado_obra": c.certificado_obra.obra_nombre,
        "certificado_empresa": c.certificado_obra.obra_empresa.empresa_nombre,
        "certificado_expediente": c.certificado_expediente,
        "certificado_fecha": c.certificado_fecha.isoformat() if c.certificado_fecha else "",
        "certificado_financiamiento": c.get_certificado_financiamiento_display(),
        "certificado_rubro_db": c.certificado_rubro_db.certificadorubro_nombre,
        "certificado_rubro_anticipo": c.certificado_rubro_anticipo,
        "certificado_rubro_obra": c.certificado_rubro_obra,
        "certificado_rubro_devanticipo": c.certificado_rubro_devanticipo,
        "certificado_monto_cobrar": format_thousands(c.certificado_monto_cobrar),
        "certificado_monto_cobrar_uvi": format_thousands(c.certificado_monto_cobrar_uvi),
        "certificado_mes_pct": c.certificado_mes_pct,
        "acciones": acciones,
    }


@router.get("/datatables/certificados/")
@decorate_view(require_model_perm(Certificado))
def datatable_certificados(
    request,
    draw: int = 1,
    start: int = 0,
    length: int = 50,
    search: str = "",
    order_by: str = "-id",
    filters: str = "{}",
):
    qs = Certificado.objects.select_related(
        "certificado_obra__obra_empresa", "certificado_rubro_db"
    ).all()
    records_total = qs.count()

    try:
        active_filters = json.loads(filters)
    except (TypeError, ValueError):
        active_filters = {}
    for key, value in active_filters.items():
        lookup = _CERTIFICADO_DATATABLE_FILTER_FIELDS.get(key)
        if lookup and value not in (None, ""):
            qs = qs.filter(**{lookup: value})

    if search:
        qs = qs.filter(
            Q(certificado_obra__obra_nombre__icontains=search)
            | Q(certificado_obra__obra_empresa__empresa_nombre__icontains=search)
            | Q(certificado_expediente__icontains=search)
            | Q(certificado_rubro_db__certificadorubro_nombre__icontains=search)
        ).distinct()

    records_filtered = qs.count()
    qs = qs.order_by(*parse_order_by(order_by, _CERTIFICADO_DATATABLE_ORDER_FIELDS), "id")
    page = qs[start:] if length == -1 else qs[start:start + length]

    return {
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": [_certificado_datatable_row(c, request.user) for c in page],
    }


@router.get("/datatables/certificados/{id}/detalle/")
@decorate_view(require_model_perm(Certificado))
def datatable_certificados_detalle(request, id: int):
    c = get_object_or_404(Certificado.objects.select_related("certificado_obra"), id=id)
    html = render_to_string(
        "ajax_datatable/carga/certificado/render_row_details.html",
        {"model": Certificado, "object": c},
        request=request,
    )
    return {"html": html}


@router.get("/datatables/certificados/filtro-rubro/")
@decorate_view(require_model_perm(Certificado))
def datatable_certificados_filtro_rubro(request):
    choices = (
        Certificado.objects.values_list("certificado_rubro_db_id", "certificado_rubro_db__certificadorubro_nombre")
        .distinct()
        .order_by("certificado_rubro_db__certificadorubro_nombre")
    )
    return {"choices": list(choices)}


# --- ConjuntoLicitado ---
@router.get("/conjuntos/", response=List[ConjuntoLicitadoOut])
@decorate_view(require_model_perm(ConjuntoLicitado))
@paginate(PerPagePagination)
def list_conjuntos(request):
    return ConjuntoLicitado.objects.all().order_by("id")


@router.get("/conjunto/{id}/", response=ConjuntoLicitadoOut)
@decorate_view(require_model_perm(ConjuntoLicitado))
def retrieve_conjunto(request, id: int):
    return get_object_or_404(ConjuntoLicitado, id=id)


@router.post("/conjuntos/", response=ConjuntoLicitadoOut)
@decorate_view(require_model_perm(ConjuntoLicitado))
def create_conjunto(request, payload: ConjuntoLicitadoCreate):
    return ConjuntoLicitado.objects.create(**payload.model_dump())


@router.put("/conjunto/{id}/", response=ConjuntoLicitadoOut)
@decorate_view(require_model_perm(ConjuntoLicitado))
def update_conjunto(request, id: int, payload: ConjuntoLicitadoUpdate):
    c = get_object_or_404(ConjuntoLicitado, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(c, field, value)
    c.save()
    return c


@router.delete("/conjunto/{id}/")
@decorate_view(require_model_perm(ConjuntoLicitado))
def delete_conjunto(request, id: int):
    deleted, _ = ConjuntoLicitado.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


def _conjunto_datatable_row(c: ConjuntoLicitado, user) -> dict:
    id_ = str(c.id)
    editarlink = f"<a href='/obra/crear/conjunto/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href='#'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/obra/eliminar/conjunto/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("carga.delete_conjunto"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("carga.change_conjunto"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {
        "id": c.id,
        "conjunto_nombre": c.conjunto_nombre,
        "conjunto_resolucion": c.conjunto_resolucion,
        "conjunto_subconjunto": c.conjunto_subconjunto.conjunto_nombre if c.conjunto_subconjunto_id else "",
        "acciones": acciones,
    }


register_simple_datatable(
    router, ConjuntoLicitado, "conjuntos",
    order_fields={
        "id": "id", "conjunto_nombre": "conjunto_nombre", "conjunto_resolucion": "conjunto_resolucion",
        "conjunto_subconjunto": "conjunto_subconjunto__conjunto_nombre",
    },
    filter_fields={
        "conjunto_nombre": "conjunto_nombre__icontains", "conjunto_resolucion": "conjunto_resolucion__icontains",
        "conjunto_subconjunto": "conjunto_subconjunto__conjunto_nombre__icontains",
    },
    search_lookups=[
        "conjunto_nombre__icontains", "conjunto_resolucion__icontains",
        "conjunto_subconjunto__conjunto_nombre__icontains",
    ],
    row_builder=_conjunto_datatable_row,
    queryset=ConjuntoLicitado.objects.select_related("conjunto_subconjunto"),
)


# --- PlanDeTrabajos ---
@router.get("/planes/", response=List[PlanDeTrabajosOut])
@decorate_view(require_model_perm(PlanDeTrabajos))
@paginate(PerPagePagination)
def list_planes(request, obra: str = ""):
    qs = PlanDeTrabajos.objects.all().order_by("-id")
    if obra:
        qs = qs.filter(trabajos_obra_id=obra)
    return qs


@router.get("/plan/{id}/", response=PlanDeTrabajosOut)
@decorate_view(require_model_perm(PlanDeTrabajos))
def retrieve_plan(request, id: int):
    return get_object_or_404(PlanDeTrabajos, id=id)


@router.post("/planes/", response=PlanDeTrabajosOut)
@decorate_view(require_model_perm(PlanDeTrabajos))
def create_plan(request, payload: PlanDeTrabajosCreate):
    return PlanDeTrabajos.objects.create(**payload.model_dump())


@router.put("/plan/{id}/", response=PlanDeTrabajosOut)
@decorate_view(require_model_perm(PlanDeTrabajos))
def update_plan(request, id: int, payload: PlanDeTrabajosUpdate):
    p = get_object_or_404(PlanDeTrabajos, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(p, field, value)
    p.save()
    return p


@router.delete("/plan/{id}/")
@decorate_view(require_model_perm(PlanDeTrabajos))
def delete_plan(request, id: int):
    deleted, _ = PlanDeTrabajos.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Contrato ---
@router.get("/contratos/", response=List[ContratoOut])
@decorate_view(require_model_perm(Contrato))
@paginate(PerPagePagination)
def list_contratos(request, obra: str = ""):
    qs = Contrato.objects.select_related("contrato_obra").all().order_by("-id")
    if obra:
        qs = qs.filter(contrato_obra_id=obra)
    return qs


@router.get("/contrato/{id}/", response=ContratoOut)
@decorate_view(require_model_perm(Contrato))
def retrieve_contrato(request, id: int):
    return get_object_or_404(Contrato, id=id)


@router.post("/contratos/", response=ContratoOut)
@decorate_view(require_model_perm(Contrato))
def create_contrato(request, payload: ContratoCreate):
    return Contrato.objects.create(**payload.model_dump())


@router.put("/contrato/{id}/", response=ContratoOut)
@decorate_view(require_model_perm(Contrato))
def update_contrato(request, id: int, payload: ContratoUpdate):
    c = get_object_or_404(Contrato, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(c, field, value)
    c.save()
    return c


@router.delete("/contrato/{id}/")
@decorate_view(require_model_perm(Contrato))
def delete_contrato(request, id: int):
    deleted, _ = Contrato.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- ContratoMonto ---
@router.get("/contratos-montos/", response=List[ContratoMontoOut])
@decorate_view(require_model_perm(ContratoMonto))
@paginate(PerPagePagination)
def list_contratos_montos(request, contrato: str = ""):
    qs = ContratoMonto.objects.all().order_by("-id")
    if contrato:
        qs = qs.filter(contratomonto_contrato_id=contrato)
    return qs


@router.post("/contratos-montos/", response=ContratoMontoOut)
@decorate_view(require_model_perm(ContratoMonto))
def create_contrato_monto(request, payload: ContratoMontoCreate):
    return ContratoMonto.objects.create(**payload.model_dump())


@router.put("/contrato-monto/{id}/", response=ContratoMontoOut)
@decorate_view(require_model_perm(ContratoMonto))
def update_contrato_monto(request, id: int, payload: ContratoMontoUpdate):
    cm = get_object_or_404(ContratoMonto, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(cm, field, value)
    cm.save()
    return cm


@router.delete("/contrato-monto/{id}/")
@decorate_view(require_model_perm(ContratoMonto))
def delete_contrato_monto(request, id: int):
    deleted, _ = ContratoMonto.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- ContratoRubro ---
@router.get("/contrato-rubros/", response=List[ContratoRubroOut])
@decorate_view(require_model_perm(ContratoRubro))
@paginate(PerPagePagination)
def list_contrato_rubros(request):
    return ContratoRubro.objects.all().order_by("contratorubro_tipo")


@router.post("/contrato-rubros/", response=ContratoRubroOut)
@decorate_view(require_model_perm(ContratoRubro))
def create_contrato_rubro(request, payload: ContratoRubroCreate):
    return ContratoRubro.objects.create(**payload.model_dump())


@router.put("/contrato-rubro/{id}/", response=ContratoRubroOut)
@decorate_view(require_model_perm(ContratoRubro))
def update_contrato_rubro(request, id: int, payload: ContratoRubroUpdate):
    cr = get_object_or_404(ContratoRubro, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(cr, field, value)
    cr.save()
    return cr


@router.delete("/contrato-rubro/{id}/")
@decorate_view(require_model_perm(ContratoRubro))
def delete_contrato_rubro(request, id: int):
    deleted, _ = ContratoRubro.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- ContratosDigitales ---
@router.get("/contratos-digitales/", response=List[ContratosDigitalesOut])
@decorate_view(require_model_perm(ContratosDigitales))
@paginate(PerPagePagination)
def list_contratos_digitales(request):
    return ContratosDigitales.objects.all().order_by("-id")


@router.post("/contratos-digitales/", response=ContratosDigitalesOut)
@decorate_view(require_model_perm(ContratosDigitales))
def create_contrato_digital(request, payload: ContratosDigitalesCreate):
    return ContratosDigitales.objects.create(**payload.model_dump())


@router.put("/contrato-digital/{id}/", response=ContratosDigitalesOut)
@decorate_view(require_model_perm(ContratosDigitales))
def update_contrato_digital(request, id: int, payload: ContratosDigitalesUpdate):
    cd = get_object_or_404(ContratosDigitales, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(cd, field, value)
    cd.save()
    return cd


@router.delete("/contrato-digital/{id}/")
@decorate_view(require_model_perm(ContratosDigitales))
def delete_contrato_digital(request, id: int):
    deleted, _ = ContratosDigitales.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- ResolucionesDigitales ---
@router.get("/resoluciones-digitales/", response=List[ResolucionesDigitalesOut])
@decorate_view(require_model_perm(ResolucionesDigitales))
@paginate(PerPagePagination)
def list_resoluciones_digitales(request):
    return ResolucionesDigitales.objects.all().order_by("-id")


@router.post("/resoluciones-digitales/", response=ResolucionesDigitalesOut)
@decorate_view(require_model_perm(ResolucionesDigitales))
def create_resolucion_digital(request, payload: ResolucionesDigitalesCreate):
    return ResolucionesDigitales.objects.create(**payload.model_dump())


@router.put("/resolucion-digital/{id}/", response=ResolucionesDigitalesOut)
@decorate_view(require_model_perm(ResolucionesDigitales))
def update_resolucion_digital(request, id: int, payload: ResolucionesDigitalesUpdate):
    rd = get_object_or_404(ResolucionesDigitales, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(rd, field, value)
    rd.save()
    return rd


@router.delete("/resolucion-digital/{id}/")
@decorate_view(require_model_perm(ResolucionesDigitales))
def delete_resolucion_digital(request, id: int):
    deleted, _ = ResolucionesDigitales.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Uvi ---
@router.get("/uvi/", response=List[UviOut])
@decorate_view(require_model_perm(Uvi))
@paginate(PerPagePagination)
def list_uvi(request):
    return Uvi.objects.all().order_by("-uvi_fecha")


@router.get("/uvi-latest/", response=UviOut)
@decorate_view(require_model_perm(Uvi))
def latest_uvi(request):
    u = Uvi.objects.order_by("-uvi_fecha").first()
    if u is None:
        raise Http404
    return u


@router.post("/uvi/", response=UviOut)
@decorate_view(require_model_perm(Uvi))
def create_uvi(request, payload: UviCreate):
    return Uvi.objects.create(**payload.model_dump())


@router.put("/uvi/{id}/", response=UviOut)
@decorate_view(require_model_perm(Uvi))
def update_uvi(request, id: int, payload: UviUpdate):
    u = get_object_or_404(Uvi, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(u, field, value)
    u.save()
    return u


@router.delete("/uvi/{id}/")
@decorate_view(require_model_perm(Uvi))
def delete_uvi(request, id: int):
    deleted, _ = Uvi.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- INDEC ---
@router.get("/indec/", response=List[INDECOut])
@decorate_view(require_model_perm(INDEC))
@paginate(PerPagePagination)
def list_indec(request):
    return INDEC.objects.all().order_by("-mes")


@router.get("/indec-latest/", response=INDECOut)
@decorate_view(require_model_perm(INDEC))
def latest_indec(request):
    i = INDEC.objects.order_by("-mes").first()
    if i is None:
        raise Http404
    return i


@router.post("/indec/", response=INDECOut)
@decorate_view(require_model_perm(INDEC))
def create_indec(request, payload: INDECCreate):
    return INDEC.objects.create(**payload.model_dump())


@router.put("/indec/{id}/", response=INDECOut)
@decorate_view(require_model_perm(INDEC))
def update_indec(request, id: int, payload: INDECUpdate):
    i = get_object_or_404(INDEC, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(i, field, value)
    i.save()
    return i


@router.delete("/indec/{id}/")
@decorate_view(require_model_perm(INDEC))
def delete_indec(request, id: int):
    deleted, _ = INDEC.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Poliza ---
@router.get("/polizas/", response=List[PolizaOut])
@decorate_view(require_model_perm(Poliza))
@paginate(PerPagePagination)
def list_polizas(request):
    return Poliza.objects.select_related(
        "poliza_aseguradora", "poliza_tomador", "poliza_obra"
    ).all().order_by("-id")


@router.get("/poliza/{id}/", response=PolizaOut)
@decorate_view(require_model_perm(Poliza))
def retrieve_poliza(request, id: int):
    return get_object_or_404(
        Poliza.objects.select_related("poliza_aseguradora", "poliza_tomador", "poliza_obra"),
        id=id,
    )


@router.post("/polizas/", response=PolizaOut)
@decorate_view(require_model_perm(Poliza))
def create_poliza(request, payload: PolizaCreate):
    return Poliza.objects.create(**payload.model_dump())


@router.put("/poliza/{id}/", response=PolizaOut)
@decorate_view(require_model_perm(Poliza))
def update_poliza(request, id: int, payload: PolizaUpdate):
    p = get_object_or_404(Poliza, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(p, field, value)
    p.save()
    return p


@router.delete("/poliza/{id}/")
@decorate_view(require_model_perm(Poliza))
def delete_poliza(request, id: int):
    deleted, _ = Poliza.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


def _poliza_datatable_row(p: Poliza, user) -> dict:
    id_ = str(p.id)
    editarlink = f"<a href='/obra/crear/poliza/{id_}'>{editlinkimg}</a>"
    detallelink = f"<a href='/obra/crear/poliza/estado/{id_}'>{detallelinkimg}</a>"
    eliminarlink = f"<a href='/obra/eliminar/poliza/{id_}'>{eliminarlinkimg}</a>"
    if user.has_perm("carga.delete_poliza"):
        acciones = f"{editarlink}{detallelink}{eliminarlink}"
    elif user.has_perm("carga.change_poliza"):
        acciones = f"{editarlink}{detallelink}"
    else:
        acciones = detallelink
    return {
        "id": p.id,
        "poliza_fecha": p.poliza_fecha.isoformat() if p.poliza_fecha else "",
        "poliza_expediente": p.poliza_expediente,
        "poliza_numero": p.poliza_numero,
        "poliza_concepto": p.get_poliza_concepto_display(),
        "poliza_recibo": p.poliza_recibo,
        "poliza_aseguradora": p.poliza_aseguradora.aseguradora_nombre,
        "poliza_tomador": p.poliza_tomador.empresa_nombre,
        "poliza_obra": p.poliza_obra.obra_nombre,
        # Columna heredada de ajax_datatable que nunca se llegó a completar en
        # customize_row (poliza_editor no es un campo del modelo); se preserva
        # vacía para no alterar el comportamiento previo.
        "poliza_editor": "",
        "acciones": acciones,
    }


register_simple_datatable(
    router, Poliza, "polizas",
    order_fields={
        "id": "id",
        "poliza_fecha": "poliza_fecha",
        "poliza_expediente": "poliza_expediente",
        "poliza_numero": "poliza_numero",
        "poliza_concepto": "poliza_concepto",
        "poliza_recibo": "poliza_recibo",
        "poliza_aseguradora": "poliza_aseguradora__aseguradora_nombre",
        "poliza_tomador": "poliza_tomador__empresa_nombre",
        "poliza_obra": "poliza_obra__obra_nombre",
    },
    filter_fields={
        "poliza_fecha": "poliza_fecha",
        "poliza_expediente": "poliza_expediente__icontains",
        "poliza_numero": "poliza_numero__icontains",
        "poliza_concepto": "poliza_concepto__icontains",
        "poliza_recibo": "poliza_recibo__icontains",
        "poliza_aseguradora": "poliza_aseguradora__aseguradora_nombre__icontains",
        "poliza_tomador": "poliza_tomador__empresa_nombre__icontains",
        "poliza_obra": "poliza_obra__obra_nombre__icontains",
    },
    search_lookups=[
        "poliza_expediente__icontains", "poliza_numero__icontains", "poliza_recibo__icontains",
        "poliza_aseguradora__aseguradora_nombre__icontains", "poliza_tomador__empresa_nombre__icontains",
        "poliza_obra__obra_nombre__icontains",
    ],
    row_builder=_poliza_datatable_row,
    default_order="-id",
    queryset=Poliza.objects.select_related("poliza_aseguradora", "poliza_tomador", "poliza_obra"),
)


# --- Poliza_Movimiento ---
@router.get("/movimientos/", response=List[PolizaMovimientoOut])
@decorate_view(require_model_perm(Poliza_Movimiento))
@paginate(PerPagePagination)
def list_movimientos(request):
    return Poliza_Movimiento.objects.select_related(
        "poliza_movimiento_receptor", "poliza_movimiento_area", "poliza_movimiento_numero"
    ).all().order_by("-id")


@router.get("/movimiento/{id}/", response=PolizaMovimientoOut)
@decorate_view(require_model_perm(Poliza_Movimiento))
def retrieve_movimiento(request, id: int):
    return get_object_or_404(Poliza_Movimiento, id=id)


@router.post("/movimientos/", response=PolizaMovimientoOut)
@decorate_view(require_model_perm(Poliza_Movimiento))
def create_movimiento(request, payload: PolizaMovimientoCreate):
    return Poliza_Movimiento.objects.create(**payload.model_dump())


@router.put("/movimiento/{id}/", response=PolizaMovimientoOut)
@decorate_view(require_model_perm(Poliza_Movimiento))
def update_movimiento(request, id: int, payload: PolizaMovimientoUpdate):
    m = get_object_or_404(Poliza_Movimiento, id=id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(m, field, value)
    m.save()
    return m


@router.delete("/movimiento/{id}/")
@decorate_view(require_model_perm(Poliza_Movimiento))
def delete_movimiento(request, id: int):
    deleted, _ = Poliza_Movimiento.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}
