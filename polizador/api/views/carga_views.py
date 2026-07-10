# carga app API views
from typing import List

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.decorators import decorate_view
from ninja.pagination import paginate

from api.permissions import get_group_perms, require_model_perm
from api.views.generics import PerPagePagination
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
