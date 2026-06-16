# carga app API views
from django.db.models import Q
from typing import Optional, List
import datetime
from api.router import api
from api.permissions import require_auth, get_group_perms

def _parse_date(s):
    if not s:
        return None
    try:
        return datetime.date.fromisoformat(s)
    except (ValueError, TypeError):
        return None


# --- Receptor ---
@api.get("/receptores/", tags=["carga"])
def list_receptores(request):
    user = require_auth(request)
    from carga.models import Receptor

    qs = Receptor.objects.all().order_by("receptor_nombre")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": r.id,
            "receptor_nombre": r.receptor_nombre,
            "receptor_uuid": str(r.receptor_uuid),
        }
        for r in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/receptor/{id}/", tags=["carga"])
def retrieve_receptor(request, id: int):
    require_auth(request)
    from carga.models import Receptor

    r = Receptor.objects.filter(id=id).first()
    if not r:
        return {"detail": "Not found"}, 404
    return {
        "id": r.id,
        "receptor_nombre": r.receptor_nombre,
        "receptor_uuid": str(r.receptor_uuid),
    }


@api.post("/receptores/", tags=["carga"])
def create_receptor(request, payload: dict):
    require_auth(request)
    from carga.models import Receptor

    r = Receptor.objects.create(
        receptor_nombre=payload.get("receptor_nombre", "")
    )
    return {
        "id": r.id,
        "receptor_nombre": r.receptor_nombre,
        "receptor_uuid": str(r.receptor_uuid),
    }


@api.put("/receptor/{id}/", tags=["carga"])
def update_receptor(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Receptor

    r = Receptor.objects.filter(id=id).first()
    if not r:
        return {"detail": "Not found"}, 404
    if "receptor_nombre" in payload:
        r.receptor_nombre = payload["receptor_nombre"]
    r.save()
    return {
        "id": r.id,
        "receptor_nombre": r.receptor_nombre,
        "receptor_uuid": str(r.receptor_uuid),
    }


@api.delete("/receptor/{id}/", tags=["carga"])
def delete_receptor(request, id: int):
    require_auth(request)
    from carga.models import Receptor

    deleted, _ = Receptor.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Area ---
@api.get("/areas/", tags=["carga"])
def list_areas(request):
    user = require_auth(request)
    from carga.models import Area

    qs = Area.objects.all().order_by("area_nombre")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {"id": a.id, "area_nombre": a.area_nombre, "area_uuid": str(a.area_uuid)}
        for a in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/area/{id}/", tags=["carga"])
def retrieve_area(request, id: int):
    require_auth(request)
    from carga.models import Area

    a = Area.objects.filter(id=id).first()
    if not a:
        return {"detail": "Not found"}, 404
    return {
        "id": a.id,
        "area_nombre": a.area_nombre,
        "area_uuid": str(a.area_uuid),
    }


@api.post("/areas/", tags=["carga"])
def create_area(request, payload: dict):
    require_auth(request)
    from carga.models import Area

    a = Area.objects.create(area_nombre=payload.get("area_nombre", ""))
    return {
        "id": a.id,
        "area_nombre": a.area_nombre,
        "area_uuid": str(a.area_uuid),
    }


@api.put("/area/{id}/", tags=["carga"])
def update_area(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Area

    a = Area.objects.filter(id=id).first()
    if not a:
        return {"detail": "Not found"}, 404
    if "area_nombre" in payload:
        a.area_nombre = payload["area_nombre"]
    a.save()
    return {
        "id": a.id,
        "area_nombre": a.area_nombre,
        "area_uuid": str(a.area_uuid),
    }


@api.delete("/area/{id}/", tags=["carga"])
def delete_area(request, id: int):
    require_auth(request)
    from carga.models import Area

    deleted, _ = Area.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Aseguradora ---
@api.get("/aseguradoras/", tags=["carga"])
def list_aseguradoras(request):
    user = require_auth(request)
    from carga.models import Aseguradora

    qs = Aseguradora.objects.all().order_by("aseguradora_nombre")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": a.id,
            "aseguradora_nombre": a.aseguradora_nombre,
            "aseguradora_uuid": str(a.aseguradora_uuid),
        }
        for a in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/aseguradora/{id}/", tags=["carga"])
def retrieve_aseguradora(request, id: int):
    require_auth(request)
    from carga.models import Aseguradora

    a = Aseguradora.objects.filter(id=id).first()
    if not a:
        return {"detail": "Not found"}, 404
    return {
        "id": a.id,
        "aseguradora_nombre": a.aseguradora_nombre,
        "aseguradora_uuid": str(a.aseguradora_uuid),
    }


@api.post("/aseguradoras/", tags=["carga"])
def create_aseguradora(request, payload: dict):
    require_auth(request)
    from carga.models import Aseguradora

    a = Aseguradora.objects.create(
        aseguradora_nombre=payload.get("aseguradora_nombre", "")
    )
    return {
        "id": a.id,
        "aseguradora_nombre": a.aseguradora_nombre,
        "aseguradora_uuid": str(a.aseguradora_uuid),
    }


@api.put("/aseguradora/{id}/", tags=["carga"])
def update_aseguradora(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Aseguradora

    a = Aseguradora.objects.filter(id=id).first()
    if not a:
        return {"detail": "Not found"}, 404
    if "aseguradora_nombre" in payload:
        a.aseguradora_nombre = payload["aseguradora_nombre"]
    a.save()
    return {
        "id": a.id,
        "aseguradora_nombre": a.aseguradora_nombre,
        "aseguradora_uuid": str(a.aseguradora_uuid),
    }


@api.delete("/aseguradora/{id}/", tags=["carga"])
def delete_aseguradora(request, id: int):
    require_auth(request)
    from carga.models import Aseguradora

    deleted, _ = Aseguradora.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Empresa ---
@api.get("/empresas/", tags=["carga"])
def list_empresas(request):
    user = require_auth(request)
    from carga.models import Empresa

    qs = Empresa.objects.all().order_by("empresa_nombre")
    search = request.GET.get("q", "").strip()
    if search:
        qs = qs.filter(
            Q(empresa_nombre__icontains=search)
            | Q(empresa_cuit__icontains=search)
            | Q(empresa_titular_nombre__icontains=search)
        )
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": e.id,
            "empresa_nombre": e.empresa_nombre,
            "empresa_cuit": e.empresa_cuit,
            "empresa_titular_nombre": e.empresa_titular_nombre,
            "empresa_uuid": str(e.empresa_uuid),
        }
        for e in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/empresa/{id}/", tags=["carga"])
def retrieve_empresa(request, id: int):
    require_auth(request)
    from carga.models import Empresa

    e = Empresa.objects.filter(id=id).first()
    if not e:
        return {"detail": "Not found"}, 404
    return {
        "id": e.id,
        "empresa_nombre": e.empresa_nombre,
        "empresa_cuit": e.empresa_cuit,
        "empresa_titular_nombre": e.empresa_titular_nombre,
        "empresa_titular_dni": float(e.empresa_titular_dni) if e.empresa_titular_dni else None,
        "empresa_direccion": e.empresa_direccion,
        "empresa_inscripcion": e.empresa_inscripcion,
        "empresa_correo_p": e.empresa_correo_p,
        "empresa_correo_s": e.empresa_correo_s,
        "empresa_uuid": str(e.empresa_uuid),
    }


@api.post("/empresas/", tags=["carga"])
def create_empresa(request, payload: dict):
    require_auth(request)
    from carga.models import Empresa

    e = Empresa.objects.create(
        empresa_nombre=payload.get("empresa_nombre", ""),
        empresa_cuit=payload.get("empresa_cuit"),
        empresa_titular_titulo=payload.get("empresa_titular_titulo"),
        empresa_titular_nombre=payload.get("empresa_titular_nombre"),
        empresa_titular_dni=payload.get("empresa_titular_dni"),
        empresa_direccion=payload.get("empresa_direccion"),
        empresa_inscripcion=payload.get("empresa_inscripcion"),
        empresa_correo_p=payload.get("empresa_correo_p"),
        empresa_correo_s=payload.get("empresa_correo_s"),
    )
    return {
        "id": e.id,
        "empresa_nombre": e.empresa_nombre,
        "empresa_uuid": str(e.empresa_uuid),
    }


@api.put("/empresa/{id}/", tags=["carga"])
def update_empresa(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Empresa

    e = Empresa.objects.filter(id=id).first()
    if not e:
        return {"detail": "Not found"}, 404
    for field in [
        "empresa_nombre", "empresa_cuit", "empresa_titular_titulo",
        "empresa_titular_nombre", "empresa_titular_dni",
        "empresa_direccion", "empresa_inscripcion",
        "empresa_correo_p", "empresa_correo_s",
    ]:
        if field in payload:
            setattr(e, field, payload[field])
    e.save()
    return {
        "id": e.id,
        "empresa_nombre": e.empresa_nombre,
        "empresa_uuid": str(e.empresa_uuid),
    }


@api.delete("/empresa/{id}/", tags=["carga"])
def delete_empresa(request, id: int):
    require_auth(request)
    from carga.models import Empresa

    deleted, _ = Empresa.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Programa ---
@api.get("/programas/", tags=["carga"])
def list_programas(request):
    user = require_auth(request)
    from carga.models import Programa

    qs = Programa.objects.all().order_by("programa_nombre")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {"id": p.id, "programa_nombre": p.programa_nombre, "programa_uuid": str(p.programa_uuid)}
        for p in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/programa/{id}/", tags=["carga"])
def retrieve_programa(request, id: int):
    require_auth(request)
    from carga.models import Programa

    p = Programa.objects.filter(id=id).first()
    if not p:
        return {"detail": "Not found"}, 404
    return {
        "id": p.id,
        "programa_nombre": p.programa_nombre,
        "programa_uuid": str(p.programa_uuid),
    }


@api.post("/programas/", tags=["carga"])
def create_programa(request, payload: dict):
    require_auth(request)
    from carga.models import Programa

    p = Programa.objects.create(programa_nombre=payload.get("programa_nombre", ""))
    return {
        "id": p.id,
        "programa_nombre": p.programa_nombre,
        "programa_uuid": str(p.programa_uuid),
    }


@api.put("/programa/{id}/", tags=["carga"])
def update_programa(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Programa

    p = Programa.objects.filter(id=id).first()
    if not p:
        return {"detail": "Not found"}, 404
    if "programa_nombre" in payload:
        p.programa_nombre = payload["programa_nombre"]
    p.save()
    return {
        "id": p.id,
        "programa_nombre": p.programa_nombre,
        "programa_uuid": str(p.programa_uuid),
    }


@api.delete("/programa/{id}/", tags=["carga"])
def delete_programa(request, id: int):
    require_auth(request)
    from carga.models import Programa

    deleted, _ = Programa.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Provincia ---
@api.get("/provincias/", tags=["carga"])
def list_provincias(request):
    user = require_auth(request)
    from carga.models import Provincia

    qs = Provincia.objects.all().order_by("provincia_nombre")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": p.id,
            "provincia_nombre": p.provincia_nombre,
            "provincia_uuid": str(p.provincia_uuid),
        }
        for p in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/provincia/{id}/", tags=["carga"])
def retrieve_provincia(request, id: int):
    require_auth(request)
    from carga.models import Provincia

    p = Provincia.objects.filter(id=id).first()
    if not p:
        return {"detail": "Not found"}, 404
    return {
        "id": p.id,
        "provincia_nombre": p.provincia_nombre,
        "provincia_uuid": str(p.provincia_uuid),
    }


@api.post("/provincias/", tags=["carga"])
def create_provincia(request, payload: dict):
    require_auth(request)
    from carga.models import Provincia

    p = Provincia.objects.create(provincia_nombre=payload.get("provincia_nombre", ""))
    return {
        "id": p.id,
        "provincia_nombre": p.provincia_nombre,
        "provincia_uuid": str(p.provincia_uuid),
    }


@api.put("/provincia/{id}/", tags=["carga"])
def update_provincia(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Provincia

    p = Provincia.objects.filter(id=id).first()
    if not p:
        return {"detail": "Not found"}, 404
    if "provincia_nombre" in payload:
        p.provincia_nombre = payload["provincia_nombre"]
    p.save()
    return {
        "id": p.id,
        "provincia_nombre": p.provincia_nombre,
        "provincia_uuid": str(p.provincia_uuid),
    }


@api.delete("/provincia/{id}/", tags=["carga"])
def delete_provincia(request, id: int):
    require_auth(request)
    from carga.models import Provincia

    deleted, _ = Provincia.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Region ---
@api.get("/regiones/", tags=["carga"])
def list_regiones(request):
    user = require_auth(request)
    from carga.models import Region

    qs = Region.objects.all().order_by("id")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {"id": r.id, "region_numero": r.region_numero, "region_uuid": str(r.region_uuid)}
        for r in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/region/{id}/", tags=["carga"])
def retrieve_region(request, id: int):
    require_auth(request)
    from carga.models import Region

    r = Region.objects.filter(id=id).first()
    if not r:
        return {"detail": "Not found"}, 404
    return {
        "id": r.id,
        "region_numero": r.region_numero,
        "region_uuid": str(r.region_uuid),
    }


@api.post("/regiones/", tags=["carga"])
def create_region(request, payload: dict):
    require_auth(request)
    from carga.models import Region

    r = Region.objects.create(region_numero=payload.get("region_numero", ""))
    return {
        "id": r.id,
        "region_numero": r.region_numero,
        "region_uuid": str(r.region_uuid),
    }


@api.put("/region/{id}/", tags=["carga"])
def update_region(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Region

    r = Region.objects.filter(id=id).first()
    if not r:
        return {"detail": "Not found"}, 404
    if "region_numero" in payload:
        r.region_numero = payload["region_numero"]
    r.save()
    return {
        "id": r.id,
        "region_numero": r.region_numero,
        "region_uuid": str(r.region_uuid),
    }


@api.delete("/region/{id}/", tags=["carga"])
def delete_region(request, id: int):
    require_auth(request)
    from carga.models import Region

    deleted, _ = Region.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Departamento (carga) ---
@api.get("/departamentos-carga/", tags=["carga"])
def list_departamentos_carga(request):
    user = require_auth(request)
    from carga.models import Departamento

    qs = Departamento.objects.all().order_by("departamento_nombre")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": d.id,
            "departamento_nombre": d.departamento_nombre,
            "departamento_uuid": str(d.departamento_uuid),
        }
        for d in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/departamento-carga/{id}/", tags=["carga"])
def retrieve_departamento_carga(request, id: int):
    require_auth(request)
    from carga.models import Departamento

    d = Departamento.objects.filter(id=id).first()
    if not d:
        return {"detail": "Not found"}, 404
    return {
        "id": d.id,
        "departamento_nombre": d.departamento_nombre,
        "departamento_uuid": str(d.departamento_uuid),
    }


@api.post("/departamentos-carga/", tags=["carga"])
def create_departamento_carga(request, payload: dict):
    require_auth(request)
    from carga.models import Departamento

    d = Departamento.objects.create(departamento_nombre=payload.get("departamento_nombre", ""))
    return {
        "id": d.id,
        "departamento_nombre": d.departamento_nombre,
        "departamento_uuid": str(d.departamento_uuid),
    }


@api.put("/departamento-carga/{id}/", tags=["carga"])
def update_departamento_carga(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Departamento

    d = Departamento.objects.filter(id=id).first()
    if not d:
        return {"detail": "Not found"}, 404
    if "departamento_nombre" in payload:
        d.departamento_nombre = payload["departamento_nombre"]
    d.save()
    return {
        "id": d.id,
        "departamento_nombre": d.departamento_nombre,
        "departamento_uuid": str(d.departamento_uuid),
    }


@api.delete("/departamento-carga/{id}/", tags=["carga"])
def delete_departamento_carga(request, id: int):
    require_auth(request)
    from carga.models import Departamento

    deleted, _ = Departamento.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Municipio ---
@api.get("/municipios/", tags=["carga"])
def list_municipios(request):
    user = require_auth(request)
    from carga.models import Municipio

    qs = Municipio.objects.all().order_by("municipio_nombre")
    dept_filter = request.GET.get("departamento", "")
    if dept_filter:
        qs = qs.filter(municipio_departamento_id=dept_filter)
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": m.id,
            "municipio_nombre": m.municipio_nombre,
            "municipio_uuid": str(m.municipio_uuid),
            "municipio_departamento": m.municipio_departamento_id,
            "municipio_region": m.municipio_region_id,
        }
        for m in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/municipio/{id}/", tags=["carga"])
def retrieve_municipio(request, id: int):
    require_auth(request)
    from carga.models import Municipio

    m = Municipio.objects.filter(id=id).first()
    if not m:
        return {"detail": "Not found"}, 404
    return {
        "id": m.id,
        "municipio_nombre": m.municipio_nombre,
        "municipio_uuid": str(m.municipio_uuid),
        "municipio_departamento": m.municipio_departamento_id,
        "municipio_region": m.municipio_region_id,
    }


@api.post("/municipios/", tags=["carga"])
def create_municipio(request, payload: dict):
    require_auth(request)
    from carga.models import Municipio

    m = Municipio.objects.create(
        municipio_nombre=payload.get("municipio_nombre", ""),
        municipio_departamento_id=payload.get("municipio_departamento"),
        municipio_region_id=payload.get("municipio_region"),
    )
    return {
        "id": m.id,
        "municipio_nombre": m.municipio_nombre,
        "municipio_uuid": str(m.municipio_uuid),
    }


@api.put("/municipio/{id}/", tags=["carga"])
def update_municipio(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Municipio

    m = Municipio.objects.filter(id=id).first()
    if not m:
        return {"detail": "Not found"}, 404
    for field in ["municipio_nombre", "municipio_departamento_id", "municipio_region_id"]:
        py_field = field.replace("_id", "")
        if py_field in payload:
            setattr(m, field, payload[py_field])
    m.save()
    return {
        "id": m.id,
        "municipio_nombre": m.municipio_nombre,
        "municipio_uuid": str(m.municipio_uuid),
    }


@api.delete("/municipio/{id}/", tags=["carga"])
def delete_municipio(request, id: int):
    require_auth(request)
    from carga.models import Municipio

    deleted, _ = Municipio.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Localidad ---
@api.get("/localidades/", tags=["carga"])
def list_localidades(request):
    user = require_auth(request)
    from carga.models import Localidad

    qs = Localidad.objects.all().order_by("localidad_nombre")
    dept_filter = request.GET.get("departamento", "")
    if dept_filter:
        qs = qs.filter(localidad_departamento_id=dept_filter)
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": l.id,
            "localidad_nombre": l.localidad_nombre,
            "localidad_uuid": str(l.localidad_uuid),
            "localidad_centroide_lat": float(l.localidad_centroide_lat) if l.localidad_centroide_lat else None,
            "localidad_centroide_lon": float(l.localidad_centroide_lon) if l.localidad_centroide_lon else None,
            "localidad_funcion": l.localidad_funcion,
            "localidad_departamento": l.localidad_departamento_id,
            "localidad_municipio": l.localidad_municipio_id,
        }
        for l in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/localidad/{id}/", tags=["carga"])
def retrieve_localidad(request, id: int):
    require_auth(request)
    from carga.models import Localidad

    l = Localidad.objects.filter(id=id).first()
    if not l:
        return {"detail": "Not found"}, 404
    return {
        "id": l.id,
        "localidad_nombre": l.localidad_nombre,
        "localidad_uuid": str(l.localidad_uuid),
        "localidad_centroide_lat": float(l.localidad_centroide_lat) if l.localidad_centroide_lat else None,
        "localidad_centroide_lon": float(l.localidad_centroide_lon) if l.localidad_centroide_lon else None,
        "localidad_funcion": l.localidad_funcion,
        "localidad_departamento": l.localidad_departamento_id,
        "localidad_municipio": l.localidad_municipio_id,
    }


@api.post("/localidades/", tags=["carga"])
def create_localidad(request, payload: dict):
    require_auth(request)
    from carga.models import Localidad

    l = Localidad.objects.create(
        localidad_nombre=payload.get("localidad_nombre", ""),
        localidad_centroide_lat=payload.get("localidad_centroide_lat"),
        localidad_centroide_lon=payload.get("localidad_centroide_lon"),
        localidad_funcion=payload.get("localidad_funcion"),
        localidad_departamento_id=payload.get("localidad_departamento"),
        localidad_municipio_id=payload.get("localidad_municipio"),
    )
    return {
        "id": l.id,
        "localidad_nombre": l.localidad_nombre,
        "localidad_uuid": str(l.localidad_uuid),
    }


@api.put("/localidad/{id}/", tags=["carga"])
def update_localidad(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Localidad

    l = Localidad.objects.filter(id=id).first()
    if not l:
        return {"detail": "Not found"}, 404
    for field in [
        "localidad_nombre", "localidad_centroide_lat", "localidad_centroide_lon",
        "localidad_funcion", "localidad_departamento_id", "localidad_municipio_id",
    ]:
        if field.replace("_id", "") in payload:
            setattr(l, field, payload.get(field.replace("_id", "")))
    l.save()
    return {
        "id": l.id,
        "localidad_nombre": l.localidad_nombre,
        "localidad_uuid": str(l.localidad_uuid),
    }


@api.delete("/localidad/{id}/", tags=["carga"])
def delete_localidad(request, id: int):
    require_auth(request)
    from carga.models import Localidad

    deleted, _ = Localidad.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Obra (complex model with M2M fields) ---
@api.get("/obras/", tags=["carga"])
def list_obras(request):
    user = require_auth(request)
    from carga.models import Obra

    qs = Obra.objects.select_related("obra_empresa", "obra_programa").all().order_by(
        "-id"
    )
    # Filters
    empresa_id = request.GET.get("empresa")
    programa_id = request.GET.get("programa")
    region_id = request.GET.get("region")
    search = request.GET.get("q", "").strip()

    if empresa_id:
        qs = qs.filter(obra_empresa_id=empresa_id)
    if programa_id:
        qs = qs.filter(obra_programa_id=programa_id)
    if region_id:
        qs = qs.filter(obra_region_id=region_id)
    if search:
        qs = qs.filter(
            Q(obra_nombre__icontains=search)
            | Q(expediente__icontains=search)
            | Q(obresolucion__icontains=search)
        )

    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()

    results = []
    for o in qs[start:end]:
        results.append({
            "id": o.id,
            "obra_nombre": o.obra_nombre,
            "obra_soluciones": float(o.obra_soluciones) if o.obra_soluciones else None,
            "empresa_id": o.obra_empresa_id,
            "region_id": o.obra_region_id,
            "programa_id": o.obra_programa_id,
            "convenio": o.obra_convenio,
            "expediente": o.obra_expediente,
            "resolucion": o.obra_resolucion,
            "licitacion_tipo": o.obra_licitacion_tipo,
            "licitacion_numero": float(o.obra_licitacion_numero) if o.obra_licitacion_numero else None,
            "licitacion_ano": float(o.obra_licitacion_ano) if o.obra_licitacion_ano else None,
            "fecha_entrega": str(o.obra_fecha_entrega) if o.obra_fecha_entrega else None,
            "fecha_contrato": str(o.obra_fecha_contrato) if o.obra_fecha_contrato else None,
            "contrato_total_pesos": float(o.obra_contrato_total_pesos),
            "nomenclatura": o.obra_nomenclatura,
        })

    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/obra/{id}/", tags=["carga"])
def retrieve_obra(request, id: int):
    require_auth(request)
    from carga.models import Obra

    o = (
        Obra.objects.select_related("obra_empresa", "obra_region", "obra_programa", "obra_conjunto")
        .prefetch_related(
            "obra_departamento_m.all",
            "obra_municipio_m.all",
            "obra_localidad_m.all",
            "obra_inspector.all",
        )
        .filter(id=id)
        .first()
    )
    if not o:
        return {"detail": "Not found"}, 404

    return {
        "id": o.id,
        "obra_nombre": o.obra_nombre,
        "obra_soluciones": float(o.obra_soluciones) if o.obra_soluciones else None,
        "empresa_id": o.obra_empresa_id,
        "region_id": o.obra_region_id,
        "departamento_ids": list(o.obra_departamento_m.values_list("id", flat=True)),
        "municipio_ids": list(o.obra_municipio_m.values_list("id", flat=True)),
        "localidad_ids": list(o.obra_localidad_m.values_list("id", flat=True)),
        "conjunto_id": o.obra_conjunto_id,
        "grupo": o.obra_grupo,
        "plazo": o.obra_plazo,
        "programa_id": o.obra_programa_id,
        "convenio": o.obra_convenio,
        "expediente": o.obra_expediente,
        "resolucion": o.obra_resolucion,
        "licitacion_tipo": o.obra_licitacion_tipo,
        "licitacion_numero": float(o.obra_licitacion_numero) if o.obra_licitacion_numero else None,
        "licitacion_ano": float(o.obra_licitacion_ano) if o.obra_licitacion_ano else None,
        "nomenclatura": o.obra_nomenclatura,
        "nomenclatura_plano": o.obra_nomenclatura_plano,
        "fecha_entrega": str(o.obra_fecha_entrega) if o.obra_fecha_entrega else None,
        "fecha_contrato": str(o.obra_fecha_contrato) if o.obra_fecha_contrato else None,
        "expediente_costo": o.obra_expediente_costo,
        "inspector_ids": list(o.obra_inspector.values_list("id", flat=True)),
        "observaciones": o.obra_observaciones,
        "contrato_nacion_pesos": float(o.obra_contrato_nacion_pesos),
        "contrato_nacion_uvi": float(o.obra_contrato_nacion_uvi),
        "contrato_provincia_pesos": float(o.obra_contrato_provincia_pesos),
        "contrato_total_pesos": float(o.obra_contrato_total_pesos),
        "obra_uuid": str(o.obra_uuid),
    }


@api.post("/obras/", tags=["carga"])
def create_obra(request, payload: dict):
    require_auth(request)
    from carga.models import Obra

    o = Obra.objects.create(
        obra_nombre=payload.get("obra_nombre", ""),
        obra_soluciones=payload.get("obra_soluciones"),
        obra_empresa_id=payload.get("empresa_id"),
        obra_region_id=payload.get("region_id"),
        obra_programa_id=payload.get("programa_id"),
        obra_convenio=payload.get("convenio"),
        obra_expediente=payload.get("expediente", ""),
    )

    # Handle M2M fields
    for field, model in [
        ("departamento_ids", "obra_departamento_m"),
        ("municipio_ids", "obra_municipio_m"),
        ("localidad_ids", "obra_localidad_m"),
        ("inspector_ids", "obra_inspector"),
    ]:
        ids = payload.get(field) or []
        if ids:
            getattr(o, model).set(ids)

    o.save()
    return {
        "id": o.id,
        "obra_nombre": o.obra_nombre,
        "empresa_id": o.obra_empresa_id,
        "programa_id": o.obra_programa_id,
        "expediente": o.obra_expediente,
        "obra_uuid": str(o.obra_uuid),
    }


@api.put("/obra/{id}/", tags=["carga"])
def update_obra(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Obra

    o = Obra.objects.filter(id=id).first()
    if not o:
        return {"detail": "Not found"}, 404

    simple_fields = [
        "obra_nombre", "obra_soluciones", "empresa_id", "region_id",
        "programa_id", "grupo", "plazo", "convenio", "expediente",
        "resolucion", "licitacion_tipo", "licitacion_numero",
        "licitacion_ano", "nomenclatura", "nomenclatura_plano",
        "fecha_entrega", "fecha_contrato", "expediente_costo",
        "observaciones", "conjunto_id",
    ]
    for field in simple_fields:
        if field in payload:
            setattr(o, f"obra_{field}" if not field.startswith("obra_") else field, payload[field])

    # Fix: handle plain name fields that map to obra_* columns
    rename_map = {
        "nombre": "obra_nombre", "soluciones": "obra_soluciones",
        "grupo": "obra_grupo", "plazo": "obra_plazo",
        "convenio": "obra_convenio", "expediente": "obra_expediente",
        "resolucion": "obra_resolucion",
    }

    o.save()

    # Handle M2M fields
    for field, model in [
        ("departamento_ids", "obra_departamento_m"),
        ("municipio_ids", "obra_municipio_m"),
        ("localidad_ids", "obra_localidad_m"),
        ("inspector_ids", "obra_inspector"),
    ]:
        ids = payload.get(field) or []
        if ids:
            getattr(o, model).set(ids)

    o.save()
    return {
        "id": o.id,
        "nombre": o.obra_nombre,
        "empresa_id": o.obra_empresa_id,
        "programa_id": o.obra_programa_id,
        "expediente": o.obra_expediente,
        "obra_uuid": str(o.obra_uuid),
    }


@api.delete("/obra/{id}/", tags=["carga"])
def delete_obra(request, id: int):
    require_auth(request)
    from carga.models import Obra

    deleted, _ = Obra.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Prototipo ---
@api.get("/prototipos/", tags=["carga"])
def list_prototipos(request):
    user = require_auth(request)
    from carga.models import Prototipo

    qs = Prototipo.objects.select_related("prototipo_obra").all().order_by("-id")
    obra_id = request.GET.get("obra", "")
    if obra_id:
        qs = qs.filter(prototipo_obra_id=obra_id)
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": p.id,
            "obra_id": p.prototipo_obra_id,
            "tipo": p.prototipo_tipo,
            "cantidad": float(p.prototipo_cantidad),
            "superficie": float(p.prototipo_superficie),
            "uvi": float(p.prototipo_uvi),
            "incremento": float(p.prototipo_incremento),
            "discapacitado": p.prototipo_discapacitado,
        }
        for p in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/prototipo/{id}/", tags=["carga"])
def retrieve_prototipo(request, id: int):
    require_auth(request)
    from carga.models import Prototipo

    p = Prototipo.objects.filter(id=id).first()
    if not p:
        return {"detail": "Not found"}, 404
    return {
        "id": p.id,
        "obra_id": p.prototipo_obra_id,
        "tipo": p.prototipo_tipo,
        "cantidad": float(p.prototipo_cantidad),
        "superficie": float(p.prototipo_superficie),
        "uvi": float(p.prototipo_uvi),
        "incremento": float(p.prototipo_incremento),
        "discapacitado": p.prototipo_discapacitado,
    }


@api.post("/prototipos/", tags=["carga"])
def create_prototipo(request, payload: dict):
    require_auth(request)
    from carga.models import Prototipo

    p = Prototipo.objects.create(
        prototipo_obra_id=payload.get("obra_id"),
        prototipo_tipo=payload.get("tipo", ""),
        prototipo_cantidad=payload.get("cantidad", 0),
        prototipo_superficie=payload.get("superficie", 0),
        prototipo_uvi=payload.get("uvi", 0),
        prototipo_incremento=payload.get("incremento", 0),
        prototipo_discapacitado=payload.get("discapacitado", False),
    )
    return {
        "id": p.id,
        "obra_id": p.prototipo_obra_id,
        "tipo": p.prototipo_tipo,
    }


@api.put("/prototipo/{id}/", tags=["carga"])
def update_prototipo(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Prototipo

    p = Prototipo.objects.filter(id=id).first()
    if not p:
        return {"detail": "Not found"}, 404
    for field in [
        "prototipo_obra_id", "prototipo_tipo", "prototipo_cantidad",
        "prototipo_superficie", "prototipo_uvi", "prototipo_incremento",
        "prototipo_discapacitado",
    ]:
        if field in payload:
            setattr(p, field, payload[field])
    p.save()
    return {
        "id": p.id,
        "obra_id": p.prototipo_obra_id,
        "tipo": p.prototipo_tipo,
    }


@api.delete("/prototipo/{id}/", tags=["carga"])
def delete_prototipo(request, id: int):
    require_auth(request)
    from carga.models import Prototipo

    deleted, _ = Prototipo.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Agente ---
@api.get("/agentes/", tags=["carga"])
def list_agentes(request):
    user = require_auth(request)
    from carga.models import Agente

    qs = Agente.objects.all().order_by("agente_nombre", "agente_apellido")
    search = request.GET.get("q", "").strip()
    if search:
        qs = qs.filter(
            Q(agente_nombre__icontains=search) | Q(agente_apellido__icontains=search)
        )
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": a.id,
            "nombre": a.agente_nombre,
            "apellido": a.agente_apellido,
            "dni": float(a.agente_dni) if a.agente_dni else None,
            "email": a.agente_email,
            "profesion": a.agente_profesion,
        }
        for a in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/agente/{id}/", tags=["carga"])
def retrieve_agente(request, id: int):
    require_auth(request)
    from carga.models import Agente

    a = Agente.objects.filter(id=id).first()
    if not a:
        return {"detail": "Not found"}, 404
    return {
        "id": a.id,
        "nombre": a.agente_nombre,
        "apellido": a.agente_apellido,
        "dni": float(a.agente_dni) if a.agente_dni else None,
        "telefono": a.agente_telefono,
        "email": a.agente_email,
        "profesion": a.agente_profesion,
        "matricula": a.agente_matricula,
    }


@api.post("/agentes/", tags=["carga"])
def create_agente(request, payload: dict):
    require_auth(request)
    from carga.models import Agente

    a = Agente.objects.create(
        agente_nombre=payload.get("nombre", ""),
        agente_apellido=payload.get("apellido", ""),
        agente_dni=payload.get("dni"),
        agente_telefono=payload.get("telefono"),
        agente_email=payload.get("email"),
        agente_profesion=payload.get("profesion"),
        agente_matricula=payload.get("matricula"),
    )
    a.save()  # triggers nombre_completo setter
    return {
        "id": a.id,
        "nombre": a.agente_nombre,
        "apellido": a.agente_apellido,
        "nombre_completo": a.agente_nombre_completo,
    }


@api.put("/agente/{id}/", tags=["carga"])
def update_agente(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Agente

    a = Agente.objects.filter(id=id).first()
    if not a:
        return {"detail": "Not found"}, 404
    for field in [
        "agente_nombre", "agente_apellido", "agente_dni",
        "agente_telefono", "agente_email", "agente_profesion", "agente_matricula",
    ]:
        if field.replace("agente_", "") in payload or field in payload:
            key = field.replace("agente_", "")
            val = payload.get(key) or payload.get(field)
            setattr(a, field, val)
    a.save()
    return {"id": a.id, "nombre_completo": a.agente_nombre_completo}


@api.delete("/agente/{id}/", tags=["carga"])
def delete_agente(request, id: int):
    require_auth(request)
    from carga.models import Agente

    deleted, _ = Agente.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- CertificadoRubro ---
@api.get("/rubros/", tags=["carga"])
def list_rubros(request):
    user = require_auth(request)
    from carga.models import CertificadoRubro

    qs = CertificadoRubro.objects.all().order_by("certificadorubro_nombre")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": r.id,
            "nombre": r.certificadorubro_nombre,
            "nombre_corto": r.certificadorubro_nombre_corto,
        }
        for r in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/rubro/{id}/", tags=["carga"])
def retrieve_rubro(request, id: int):
    require_auth(request)
    from carga.models import CertificadoRubro

    r = CertificadoRubro.objects.filter(id=id).first()
    if not r:
        return {"detail": "Not found"}, 404
    return {
        "id": r.id,
        "nombre": r.certificadorubro_nombre,
        "nombre_corto": r.certificadorubro_nombre_corto,
    }


@api.post("/rubros/", tags=["carga"])
def create_rubro(request, payload: dict):
    require_auth(request)
    from carga.models import CertificadoRubro

    r = CertificadoRubro.objects.create(
        certificadorubro_nombre=payload.get("nombre", ""),
        certificadorubro_nombre_corto=payload.get("nombre_corto", ""),
    )
    return {"id": r.id, "nombre": r.certificadorubro_nombre}


@api.put("/rubro/{id}/", tags=["carga"])
def update_rubro(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import CertificadoRubro

    r = CertificadoRubro.objects.filter(id=id).first()
    if not r:
        return {"detail": "Not found"}, 404
    for field in ["certificadorubro_nombre", "certificadorubro_nombre_corto"]:
        key = field.replace("certificadorubro_", "")
        if key in payload:
            setattr(r, field, payload[key])
    r.save()
    return {"id": r.id, "nombre": r.certificadorubro_nombre}


@api.delete("/rubro/{id}/", tags=["carga"])
def delete_rubro(request, id: int):
    require_auth(request)
    from carga.models import CertificadoRubro

    deleted, _ = CertificadoRubro.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- CertificadoFinanciamiento ---
@api.get("/financiamientos/", tags=["carga"])
def list_financiamientos(request):
    user = require_auth(request)
    from carga.models import CertificadoFinanciamiento

    qs = CertificadoFinanciamiento.objects.all().order_by("certificadofinanciamiento_nombre")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": f.id,
            "nombre": f.certificadofinanciamiento_nombre,
            "nombre_corto": f.certificadofinanciamiento_nombre_corto,
        }
        for f in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/financiamiento/{id}/", tags=["carga"])
def retrieve_financiamiento(request, id: int):
    require_auth(request)
    from carga.models import CertificadoFinanciamiento

    f = CertificadoFinanciamiento.objects.filter(id=id).first()
    if not f:
        return {"detail": "Not found"}, 404
    return {
        "id": f.id,
        "nombre": f.certificadofinanciamiento_nombre,
        "nombre_corto": f.certificadofinanciamiento_nombre_corto,
    }


@api.post("/financiamientos/", tags=["carga"])
def create_financiamiento(request, payload: dict):
    require_auth(request)
    from carga.models import CertificadoFinanciamiento

    f = CertificadoFinanciamiento.objects.create(
        certificadofinanciamiento_nombre=payload.get("nombre", ""),
        certificadofinanciamiento_nombre_corto=payload.get("nombre_corto", ""),
    )
    return {"id": f.id, "nombre": f.certificadofinanciamiento_nombre}


@api.put("/financiamiento/{id}/", tags=["carga"])
def update_financiamiento(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import CertificadoFinanciamiento

    f = CertificadoFinanciamiento.objects.filter(id=id).first()
    if not f:
        return {"detail": "Not found"}, 404
    for field in ["certificadofinanciamiento_nombre", "certificadofinanciamiento_nombre_corto"]:
        key = field.replace("certificadofinanciamiento_", "")
        if key in payload:
            setattr(f, field, payload[key])
    f.save()
    return {"id": f.id, "nombre": f.certificadofinanciamiento_nombre}


@api.delete("/financiamiento/{id}/", tags=["carga"])
def delete_financiamiento(request, id: int):
    require_auth(request)
    from carga.models import CertificadoFinanciamiento

    deleted, _ = CertificadoFinanciamiento.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Certificado ---
@api.get("/certificados/", tags=["carga"])
@get_group_perms("gciaoperativa_usuarios")
def list_certificados(request):
    user = require_auth(request)
    from carga.models import Certificado

    qs = Certificado.objects.select_related("certificado_obra").all().order_by(
        "-certificado_fecha"
    )
    obra_id = request.GET.get("obra", "")
    if obra_id:
        qs = qs.filter(certificado_obra_id=obra_id)
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": c.id,
            "obra_id": c.certificado_obra_id,
            "financiamiento": c.certificado_financiamiento,
            "rubro": c.certificado_rubro,
            "rubro_db_id": c.certificado_rubro_db_id,
            "expediente": c.certificado_expediente,
            "periodo": c.certificado_periodo,
            "monto_pesos": float(c.certificado_monto_pesos) if c.certificado_monto_pesos else 0.0,
            "fecha": str(c.certificado_fecha),
            "monto_cobrar": float(c.certificado_monto_cobrar) if c.certificado_monto_cobrar else 0.0,
        }
        for c in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/certificado/{id}/", tags=["carga"])
def retrieve_certificado(request, id: int):
    require_auth(request)
    from carga.models import Certificado

    c = Certificado.objects.filter(id=id).first()
    if not c:
        return {"detail": "Not found"}, 404
    return {
        "id": c.id,
        "obra_id": c.certificado_obra_id,
        "financiamiento": c.certificado_financiamiento,
        "rubro": c.certificado_rubro,
        "expediente": c.certificado_expediente,
        "periodo": c.certificado_periodo,
        "monto_pesos": float(c.certificado_monto_pesos) if c.certificado_monto_pesos else 0.0,
        "fecha": str(c.certificado_fecha),
    }


@api.post("/certificados/", tags=["carga"])
def create_certificado(request, payload: dict):
    require_auth(request)
    from carga.models import Certificado

    c = Certificado.objects.create(
        certificado_obra_id=payload.get("obra_id"),
        certificado_financiamiento=payload.get("financiamiento", "N"),
        certificado_rubro_db_id=payload.get("rubro_db_id", 1),
        certificado_expediente=payload.get("expediente", ""),
        certificado_monto_pesos=payload.get("monto_pesos", 0),
        certificado_fecha=payload.get("fecha"),
    )
    return {
        "id": c.id,
        "obra_id": c.certificado_obra_id,
        "expediente": c.certificado_expediente,
    }


@api.put("/certificado/{id}/", tags=["carga"])
def update_certificado(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Certificado

    c = Certificado.objects.filter(id=id).first()
    if not c:
        return {"detail": "Not found"}, 404
    for field in [
        "certificado_obra_id", "certificado_financiamiento",
        "certificado_rubro_db_id", "certificado_expediente",
        "certificado_monto_pesos", "certificado_fecha",
    ]:
        key = field.replace("certificado_", "")
        if key in payload:
            setattr(c, field, payload[key])
    c.save()
    return {"id": c.id}


@api.delete("/certificado/{id}/", tags=["carga"])
def delete_certificado(request, id: int):
    require_auth(request)
    from carga.models import Certificado

    deleted, _ = Certificado.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- ConjuntoLicitado ---
@api.get("/conjuntos/", tags=["carga"])
def list_conjuntos(request):
    user = require_auth(request)
    from carga.models import ConjuntoLicitado

    qs = ConjuntoLicitado.objects.all().order_by("id")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": c.id,
            "nombre": c.conjunto_nombre,
            "soluciones": float(c.conjunto_soluciones) if c.conjunto_soluciones else None,
            "resolucion": c.conjunto_resolucion,
        }
        for c in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/conjunto/{id}/", tags=["carga"])
def retrieve_conjunto(request, id: int):
    require_auth(request)
    from carga.models import ConjuntoLicitado

    c = ConjuntoLicitado.objects.filter(id=id).first()
    if not c:
        return {"detail": "Not found"}, 404
    return {
        "id": c.id,
        "nombre": c.conjunto_nombre,
        "soluciones": float(c.conjunto_soluciones) if c.conjunto_soluciones else None,
        "resolucion": c.conjunto_resolucion,
    }


@api.post("/conjuntos/", tags=["carga"])
def create_conjunto(request, payload: dict):
    require_auth(request)
    from carga.models import ConjuntoLicitado

    c = ConjuntoLicitado.objects.create(
        conjunto_nombre=payload.get("nombre", ""),
        conjunto_soluciones=payload.get("soluciones"),
        conjunto_resolucion=payload.get("resolucion"),
    )
    return {"id": c.id, "nombre": c.conjunto_nombre}


@api.put("/conjunto/{id}/", tags=["carga"])
def update_conjunto(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import ConjuntoLicitado

    c = ConjuntoLicitado.objects.filter(id=id).first()
    if not c:
        return {"detail": "Not found"}, 404
    for field in ["conjunto_nombre", "conjunto_soluciones", "conjunto_resolucion"]:
        key = field.replace("conjunto_", "")
        if key in payload:
            setattr(c, field, payload[key])
    c.save()
    return {"id": c.id}


@api.delete("/conjunto/{id}/", tags=["carga"])
def delete_conjunto(request, id: int):
    require_auth(request)
    from carga.models import ConjuntoLicitado

    deleted, _ = ConjuntoLicitado.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- PlanDeTrabajos ---
@api.get("/planes/", tags=["carga"])
def list_planes(request):
    user = require_auth(request)
    from carga.models import PlanDeTrabajos

    qs = PlanDeTrabajos.objects.all().order_by("-id")
    obra_id = request.GET.get("obra", "")
    if obra_id:
        qs = qs.filter(trabajos_obra_id=obra_id)
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {"id": p.id, "obra_id": p.trabajos_obra_id}
        for p in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/plan/{id}/", tags=["carga"])
def retrieve_plan(request, id: int):
    require_auth(request)
    from carga.models import PlanDeTrabajos

    p = PlanDeTrabajos.objects.filter(id=id).first()
    if not p:
        return {"detail": "Not found"}, 404
    return {"id": p.id, "obra_id": p.trabajos_obra_id}


@api.post("/planes/", tags=["carga"])
def create_plan(request, payload: dict):
    require_auth(request)
    from carga.models import PlanDeTrabajos

    p = PlanDeTrabajos.objects.create(trabajos_obra_id=payload.get("obra_id"))
    return {"id": p.id, "obra_id": p.trabajos_obra_id}


@api.put("/plan/{id}/", tags=["carga"])
def update_plan(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import PlanDeTrabajos

    p = PlanDeTrabajos.objects.filter(id=id).first()
    if not p:
        return {"detail": "Not found"}, 404
    if "obra_id" in payload:
        p.trabajos_obra_id = payload["obra_id"]
    p.save()
    return {"id": p.id, "obra_id": p.trabajos_obra_id}


@api.delete("/plan/{id}/", tags=["carga"])
def delete_plan(request, id: int):
    require_auth(request)
    from carga.models import PlanDeTrabajos

    deleted, _ = PlanDeTrabajos.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Contrato ---
@api.get("/contratos/", tags=["carga"])
def list_contratos(request):
    user = require_auth(request)
    from carga.models import Contrato

    qs = Contrato.objects.select_related("contrato_obra").all().order_by("-id")
    obra_id = request.GET.get("obra", "")
    if obra_id:
        qs = qs.filter(contrato_obra_id=obra_id)
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": c.id,
            "obra_id": c.contrato_obra_id,
            "fecha": str(c.contrato_fecha),
            "descripcion": c.contrato_descripcion,
            "resolucion": c.contrato_resolucion,
        }
        for c in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/contrato/{id}/", tags=["carga"])
def retrieve_contrato(request, id: int):
    require_auth(request)
    from carga.models import Contrato

    c = Contrato.objects.filter(id=id).first()
    if not c:
        return {"detail": "Not found"}, 404
    return {
        "id": c.id,
        "obra_id": c.contrato_obra_id,
        "fecha": str(c.contrato_fecha),
        "descripcion": c.contrato_descripcion,
        "resolucion": c.contrato_resolucion,
    }


@api.post("/contratos/", tags=["carga"])
def create_contrato(request, payload: dict):
    require_auth(request)
    from carga.models import Contrato

    c = Contrato.objects.create(
        contrato_obra_id=payload.get("obra_id"),
        contrato_fecha=payload.get("fecha"),
        contrato_descripcion=payload.get("descripcion", ""),
        contrato_resolucion=payload.get("resolucion"),
    )
    return {"id": c.id, "obra_id": c.contrato_obra_id}


@api.put("/contrato/{id}/", tags=["carga"])
def update_contrato(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Contrato

    c = Contrato.objects.filter(id=id).first()
    if not c:
        return {"detail": "Not found"}, 404
    for field in ["contrato_obra_id", "contrato_fecha", "contrato_descripcion", "contrato_resolucion"]:
        key = field.replace("contrato_", "")
        if key in payload:
            setattr(c, field, payload[key])
    c.save()
    return {"id": c.id}


@api.delete("/contrato/{id}/", tags=["carga"])
def delete_contrato(request, id: int):
    require_auth(request)
    from carga.models import Contrato

    deleted, _ = Contrato.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- ContratoMonto ---
@api.get("/contratos-montos/", tags=["carga"])
def list_contratos_montos(request):
    user = require_auth(request)
    from carga.models import ContratoMonto

    qs = ContratoMonto.objects.all().order_by("-id")
    contrato_id = request.GET.get("contrato", "")
    if contrato_id:
        qs = qs.filter(contratomonto_contrato_id=contrato_id)
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": cm.id,
            "contrato_id": cm.contratomonto_contrato_id,
            "rubro_id": cm.contratomonto_rubro_id,
            "financiamiento_id": cm.contratomonto_financiamiento_id,
            "pesos": float(cm.contratomonto_pesos),
        }
        for cm in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.post("/contratos-montos/", tags=["carga"])
def create_contrato_monto(request, payload: dict):
    require_auth(request)
    from carga.models import ContratoMonto

    cm = ContratoMonto.objects.create(
        contratomonto_contrato_id=payload.get("contrato_id"),
        contratomonto_rubro_id=payload.get("rubro_id"),
        contratomonto_financiamiento_id=payload.get("financiamiento_id"),
        contratomonto_pesos=payload.get("pesos", 0),
    )
    return {"id": cm.id, "contrato_id": cm.contratomonto_contrato_id}


@api.put("/contrato-monto/{id}/", tags=["carga"])
def update_contrato_monto(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import ContratoMonto

    cm = ContratoMonto.objects.filter(id=id).first()
    if not cm:
        return {"detail": "Not found"}, 404
    for field in ["contratomonto_contrato_id", "contratomonto_rubro_id", "contratomonto_financiamiento_id"]:
        key = field.replace("contratomonto_", "")
        if key in payload:
            setattr(cm, field, payload[key])
    cm.save()
    return {"id": cm.id}


@api.delete("/contrato-monto/{id}/", tags=["carga"])
def delete_contrato_monto(request, id: int):
    require_auth(request)
    from carga.models import ContratoMonto

    deleted, _ = ContratoMonto.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- ContratoRubro ---
@api.get("/contrato-rubros/", tags=["carga"])
def list_contrato_rubros(request):
    user = require_auth(request)
    from carga.models import ContratoRubro

    qs = ContratoRubro.objects.all().order_by("contratorubro_tipo")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {"id": cr.id, "tipo": cr.contratorubro_tipo}
        for cr in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.post("/contrato-rubros/", tags=["carga"])
def create_contrato_rubro(request, payload: dict):
    require_auth(request)
    from carga.models import ContratoRubro

    cr = ContratoRubro.objects.create(
        contratorubro_tipo=payload.get("tipo", "")
    )
    return {"id": cr.id}


@api.put("/contrato-rubro/{id}/", tags=["carga"])
def update_contrato_rubro(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import ContratoRubro

    cr = ContratoRubro.objects.filter(id=id).first()
    if not cr:
        return {"detail": "Not found"}, 404
    if "tipo" in payload:
        cr.contratorubro_tipo = payload["tipo"]
    cr.save()
    return {"id": cr.id}


@api.delete("/contrato-rubro/{id}/", tags=["carga"])
def delete_contrato_rubro(request, id: int):
    require_auth(request)
    from carga.models import ContratoRubro

    deleted, _ = ContratoRubro.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- ContratosDigitales ---
@api.get("/contratos-digitales/", tags=["carga"])
def list_contratos_digitales(request):
    user = require_auth(request)
    from carga.models import ContratosDigitales

    qs = ContratosDigitales.objects.all().order_by("-id")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": cd.id,
            "descripcion": cd.contratodigital_descripcion,
            "tipo_id": cd.contratodigital_tipo_id,
        }
        for cd in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.post("/contratos-digitales/", tags=["carga"])
def create_contrato_digital(request, payload: dict):
    require_auth(request)
    from carga.models import ContratosDigitales

    cd = ContratosDigitales.objects.create(
        contratodigital_descripcion=payload.get("descripcion", ""),
        contratodigital_tipo_id=payload.get("tipo_id"),
    )
    return {"id": cd.id}


@api.put("/contrato-digital/{id}/", tags=["carga"])
def update_contrato_digital(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import ContratosDigitales

    cd = ContratosDigitales.objects.filter(id=id).first()
    if not cd:
        return {"detail": "Not found"}, 404
    for field in ["contratodigital_descripcion", "contratodigital_tipo_id"]:
        key = field.replace("contratodigital_", "")
        if key in payload:
            setattr(cd, field, payload[key])
    cd.save()
    return {"id": cd.id}


@api.delete("/contrato-digital/{id}/", tags=["carga"])
def delete_contrato_digital(request, id: int):
    require_auth(request)
    from carga.models import ContratosDigitales

    deleted, _ = ContratosDigitales.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- ResolucionesDigitales ---
@api.get("/resoluciones-digitales/", tags=["carga"])
def list_resoluciones_digitales(request):
    user = require_auth(request)
    from carga.models import ResolucionesDigitales

    qs = ResolucionesDigitales.objects.all().order_by("-id")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": rd.id,
            "descripcion": rd.resoluciondigital_descripcion,
            "numero": rd.resoluciondigital_numero,
        }
        for rd in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.post("/resoluciones-digitales/", tags=["carga"])
def create_resolucion_digital(request, payload: dict):
    require_auth(request)
    from carga.models import ResolucionesDigitales

    rd = ResolucionesDigitales.objects.create(
        resoluciondigital_descripcion=payload.get("descripcion", ""),
        resoluciondigital_numero=payload.get("numero", ""),
    )
    return {"id": rd.id}


@api.put("/resolucion-digital/{id}/", tags=["carga"])
def update_resolucion_digital(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import ResolucionesDigitales

    rd = ResolucionesDigitales.objects.filter(id=id).first()
    if not rd:
        return {"detail": "Not found"}, 404
    for field in ["resoluciondigital_descripcion", "resoluciondigital_numero"]:
        key = field.replace("resoluciondigital_", "")
        if key in payload:
            setattr(rd, field, payload[key])
    rd.save()
    return {"id": rd.id}


@api.delete("/resolucion-digital/{id}/", tags=["carga"])
def delete_resolucion_digital(request, id: int):
    require_auth(request)
    from carga.models import ResolucionesDigitales

    deleted, _ = ResolucionesDigitales.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Uvi ---
@api.get("/uvi/", tags=["carga"])
def list_uvi(request):
    user = require_auth(request)
    from carga.models import Uvi

    qs = Uvi.objects.all().order_by("-uvi_fecha")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": u.id,
            "fecha": str(u.uvi_fecha),
            "valor": float(u.uvi_valor),
        }
        for u in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/uvi-latest/", tags=["carga"])
def latest_uvi(request):
    require_auth(request)
    from carga.models import Uvi

    u = Uvi.objects.latest().first()
    if not u:
        return {"detail": "Not found"}, 404
    return {
        "id": u.id,
        "fecha": str(u.uvi_fecha),
        "valor": float(u.uvi_valor),
    }


@api.post("/uvi/", tags=["carga"])
def create_uvi(request, payload: dict):
    require_auth(request)
    from carga.models import Uvi

    u = Uvi.objects.create(
        uvi_fecha=payload.get("fecha"),
        uvi_valor=payload.get("valor", 0),
    )
    return {"id": u.id}


@api.put("/uvi/{id}/", tags=["carga"])
def update_uvi(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Uvi

    u = Uvi.objects.filter(id=id).first()
    if not u:
        return {"detail": "Not found"}, 404
    for field in ["uvi_fecha", "uvi_valor"]:
        key = field.replace("uvi_", "")
        if key in payload:
            setattr(u, field, payload[key])
    u.save()
    return {"id": u.id}


@api.delete("/uvi/{id}/", tags=["carga"])
def delete_uvi(request, id: int):
    require_auth(request)
    from carga.models import Uvi

    deleted, _ = Uvi.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- INDEC ---
@api.get("/indec/", tags=["carga"])
def list_indec(request):
    user = require_auth(request)
    from carga.models import INDEC

    qs = INDEC.objects.all().order_by("-mes")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": i.id,
            "mes": str(i.mes),
            "mano_de_obra": float(i.indec_manodeobra),
            "albanileria": float(i.indec_albanileria),
            "transporte": float(i.indec_transporte),
        }
        for i in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/indec-latest/", tags=["carga"])
def latest_indec(request):
    require_auth(request)
    from carga.models import INDEC

    i = INDEC.objects.latest().first()
    if not i:
        return {"detail": "Not found"}, 404
    return {
        "id": i.id,
        "mes": str(i.mes),
        "mano_de_obra": float(i.indec_manodeobra),
    }


@api.post("/indec/", tags=["carga"])
def create_indec(request, payload: dict):
    require_auth(request)
    from carga.models import INDEC

    i = INDEC.objects.create(
        mes=payload.get("mes"),
        indec_manodeobra=payload.get("mano_de_obra", 0),
    )
    return {"id": i.id}


@api.put("/indec/{id}/", tags=["carga"])
def update_indec(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import INDEC

    i = INDEC.objects.filter(id=id).first()
    if not i:
        return {"detail": "Not found"}, 404
    for field in ["indec_manodeobra", "mes"]:
        key = field.replace("indec_", "")
        if key in payload:
            setattr(i, field, payload[key])
    i.save()
    return {"id": i.id}


@api.delete("/indec/{id}/", tags=["carga"])
def delete_indec(request, id: int):
    require_auth(request)
    from carga.models import INDEC

    deleted, _ = INDEC.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Poliza (P0 - core model) ---
@api.get("/polizas/", tags=["carga"])
def list_polizas(request):
    user = require_auth(request)
    from carga.models import Poliza

    qs = Poliza.objects.select_related(
        "poliza_aseguradora", "poliza_tomador", "poliza_obra"
    ).all().order_by("-id")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": p.id,
            "fecha": str(p.poliza_fecha),
            "expediente": p.poliza_expediente,
            "numero": p.poliza_numero,
            "concepto": p.poliza_concepto,
            "recibo": p.poliza_recibo,
            "aseguradora_id": p.poliza_aseguradora_id,
            "tomador_id": p.poliza_tomador_id,
            "obra_id": p.poliza_obra_id,
        }
        for p in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/poliza/{id}/", tags=["carga"])
def retrieve_poliza(request, id: int):
    require_auth(request)
    from carga.models import Poliza

    p = (
        Poliza.objects.select_related(
            "poliza_aseguradora", "poliza_tomador", "poliza_obra"
        )
        .filter(id=id)
        .first()
    )
    if not p:
        return {"detail": "Not found"}, 404
    return {
        "id": p.id,
        "fecha": str(p.poliza_fecha),
        "expediente": p.poliza_expediente,
        "numero": p.poliza_numero,
        "concepto": p.poliza_concepto,
        "recibo": p.poliza_recibo,
        "aseguradora_id": p.poliza_aseguradora_id,
        "tomador_id": p.poliza_tomador_id,
        "obra_id": p.poliza_obra_id,
    }


@api.post("/polizas/", tags=["carga"])
def create_poliza(request, payload: dict):
    require_auth(request)
    from carga.models import Poliza

    p = Poliza.objects.create(
        poliza_fecha=payload.get("fecha"),
        poliza_expediente=payload.get("expediente", ""),
        poliza_numero=payload.get("numero", 0),
        poliza_concepto=payload.get("concepto", "C"),
        poliza_recibo=payload.get("recibo", ""),
        poliza_aseguradora_id=payload.get("aseguradora_id"),
        poliza_tomador_id=payload.get("tomador_id"),
        poliza_obra_id=payload.get("obra_id"),
    )
    return {
        "id": p.id,
        "expediente": p.poliza_expediente,
        "numero": p.poliza_numero,
    }


@api.put("/poliza/{id}/", tags=["carga"])
def update_poliza(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Poliza

    p = Poliza.objects.filter(id=id).first()
    if not p:
        return {"detail": "Not found"}, 404
    for field in [
        "poliza_fecha", "poliza_expediente", "poliza_numero",
        "poliza_concepto", "poliza_recibo",
        "poliza_aseguradora_id", "poliza_tomador_id", "poliza_obra_id",
    ]:
        key = field.replace("poliza_", "")
        if key in payload:
            setattr(p, field, payload[key])
    p.save()
    return {"id": p.id, "expediente": p.poliza_expediente}


@api.delete("/poliza/{id}/", tags=["carga"])
def delete_poliza(request, id: int):
    require_auth(request)
    from carga.models import Poliza

    deleted, _ = Poliza.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Poliza_Movimiento ---
@api.get("/movimientos/", tags=["carga"])
def list_movimientos(request):
    user = require_auth(request)
    from carga.models import Poliza_Movimiento

    qs = Poliza_Movimiento.objects.select_related(
        "poliza_movimiento_receptor", "poliza_movimiento_area", "poliza_movimiento_numero"
    ).all().order_by("-id")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": m.id,
            "fecha": str(m.poliza_movimiento_fecha),
            "receptor_id": m.poliza_movimiento_receptor_id,
            "area_id": m.poliza_movimiento_area_id,
            "poliza_id": m.poliza_movimiento_numero_id,
        }
        for m in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/movimiento/{id}/", tags=["carga"])
def retrieve_movimiento(request, id: int):
    require_auth(request)
    from carga.models import Poliza_Movimiento

    m = Poliza_Movimiento.objects.filter(id=id).first()
    if not m:
        return {"detail": "Not found"}, 404
    return {
        "id": m.id,
        "fecha": str(m.poliza_movimiento_fecha),
        "receptor_id": m.poliza_movimiento_receptor_id,
        "area_id": m.poliza_movimiento_area_id,
        "poliza_id": m.poliza_movimiento_numero_id,
    }


@api.post("/movimientos/", tags=["carga"])
def create_movimiento(request, payload: dict):
    require_auth(request)
    from carga.models import Poliza_Movimiento

    m = Poliza_Movimiento.objects.create(
        poliza_movimiento_fecha=payload.get("fecha"),
        poliza_movimiento_receptor_id=payload.get("receptor_id"),
        poliza_movimiento_area_id=payload.get("area_id"),
        poliza_movimiento_numero_id=payload.get("poliza_id"),
    )
    return {"id": m.id}


@api.put("/movimiento/{id}/", tags=["carga"])
def update_movimiento(request, id: int, payload: dict):
    require_auth(request)
    from carga.models import Poliza_Movimiento

    m = Poliza_Movimiento.objects.filter(id=id).first()
    if not m:
        return {"detail": "Not found"}, 404
    for field in [
        "poliza_movimiento_fecha", "poliza_movimiento_receptor_id",
        "poliza_movimiento_area_id", "poliza_movimiento_numero_id",
    ]:
        key = field.replace("poliza_movimiento_", "")
        if key in payload:
            setattr(m, field, payload[key])
    m.save()
    return {"id": m.id}


@api.delete("/movimiento/{id}/", tags=["carga"])
def delete_movimiento(request, id: int):
    require_auth(request)
    from carga.models import Poliza_Movimiento

    deleted, _ = Poliza_Movimiento.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}

