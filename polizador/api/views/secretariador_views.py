# secretariador app API views
from django.db.models import Q
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


# --- CustomUser ---
@api.get("/users/", tags=["secretariador"])
def list_users(request):
    user = require_auth(request)
    from django.contrib.auth import get_user_model

    User = get_user_model()
    qs = User.objects.all().order_by("username")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": u.id,
            "username": u.username,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "email": u.email,
        }
        for u in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/user/{id}/", tags=["secretariador"])
def retrieve_user(request, id: int):
    require_auth(request)
    from django.contrib.auth import get_user_model

    User = get_user_model()
    u = User.objects.filter(id=id).first()
    if not u:
        return {"detail": "Not found"}, 404
    return {
        "id": u.id,
        "username": u.username,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "email": u.email,
    }


# --- Memorandum ---
@api.get("/memorandums/", tags=["secretariador"])
def list_memorandums(request):
    user = require_auth(request)
    from secretariador.models import InstrumentosLegalesMemorandum

    qs = InstrumentosLegalesMemorandum.objects.all().order_by("-id")
    ano_filter = request.GET.get("ano", "")
    if ano_filter:
        qs = qs.filter(instrumentolegalmemorandum_ano=ano_filter)
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": m.id,
            "tipo": m.instrumentolegalmemorandum_tipo,
            "numero": m.instrumentolegalmemorandum_numero,
            "ano": m.instrumentolegalmemorandum_ano,
            "descripcion": m.instrumentolegalmemorandum_descripcion,
        }
        for m in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/memorandum/{id}/", tags=["secretariador"])
def retrieve_memorandum(request, id: int):
    require_auth(request)
    from secretariador.models import InstrumentosLegalesMemorandum

    m = InstrumentosLegalesMemorandum.objects.filter(id=id).first()
    if not m:
        return {"detail": "Not found"}, 404
    return {
        "id": m.id,
        "tipo": m.instrumentolegalmemorandum_tipo,
        "numero": m.instrumentolegalmemorandum_numero,
        "ano": m.instrumentolegalmemorandum_ano,
        "descripcion": m.instrumentolegalmemorandum_descripcion,
    }


@api.post("/memorandums/", tags=["secretariador"])
def create_memorandum(request, payload: dict):
    require_auth(request)
    from secretariador.models import InstrumentosLegalesMemorandum

    m = InstrumentosLegalesMemorandum.objects.create(
        instrumentolegalmemorandum_tipo=payload.get("tipo", "P"),
        instrumentolegalmemorandum_numero=payload.get("numero", ""),
        instrumentolegalmemorandum_ano=payload.get("ano", ""),
        instrumentolegalmemorandum_descripcion=payload.get("descripcion", ""),
    )
    return {"id": m.id}


@api.put("/memorandum/{id}/", tags=["secretariador"])
def update_memorandum(request, id: int, payload: dict):
    require_auth(request)
    from secretariador.models import InstrumentosLegalesMemorandum

    m = InstrumentosLegalesMemorandum.objects.filter(id=id).first()
    if not m:
        return {"detail": "Not found"}, 404
    for field in ["instrumentolegalmemorandum_tipo", "instrumentolegalmemorandum_numero",
                  "instrumentolegalmemorandum_ano", "instrumentolegalmemorandum_descripcion"]:
        key = field.replace("instrumentolegalmemorandum_", "")
        if key in payload:
            setattr(m, field, payload[key])
    m.save()
    return {"id": m.id}


@api.delete("/memorandum/{id}/", tags=["secretariador"])
def delete_memorandum(request, id: int):
    require_auth(request)
    from secretariador.models import InstrumentosLegalesMemorandum

    deleted, _ = InstrumentosLegalesMemorandum.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Resoluciones ---
@api.get("/resoluciones/", tags=["secretariador"])
def list_resoluciones(request):
    user = require_auth(request)
    from secretariador.models import InstrumentosLegalesResoluciones

    qs = InstrumentosLegalesResoluciones.objects.all().order_by("-id")
    ano_filter = request.GET.get("ano", "")
    if ano_filter:
        qs = qs.filter(instrumentolegalresoluciones_ano=ano_filter)
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": r.id,
            "tipo": r.instrumentolegalresoluciones_tipo,
            "numero": r.instrumentolegalresoluciones_numero,
            "ano": r.instrumentolegalresoluciones_ano,
            "descripcion": r.instrumentolegalresoluciones_descripcion,
        }
        for r in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/resolucion/{id}/", tags=["secretariador"])
def retrieve_resolucion(request, id: int):
    require_auth(request)
    from secretariador.models import InstrumentosLegalesResoluciones

    r = InstrumentosLegalesResoluciones.objects.filter(id=id).first()
    if not r:
        return {"detail": "Not found"}, 404
    return {
        "id": r.id,
        "tipo": r.instrumentolegalresoluciones_tipo,
        "numero": r.instrumentolegalresoluciones_numero,
        "ano": r.instrumentolegalresoluciones_ano,
        "descripcion": r.instrumentolegalresoluciones_descripcion,
    }


@api.post("/resoluciones/", tags=["secretariador"])
def create_resolucion(request, payload: dict):
    require_auth(request)
    from secretariador.models import InstrumentosLegalesResoluciones

    r = InstrumentosLegalesResoluciones.objects.create(
        instrumentolegalresoluciones_tipo=payload.get("tipo", "P"),
        instrumentolegalresoluciones_numero=payload.get("numero", ""),
        instrumentolegalresoluciones_ano=payload.get("ano", ""),
        instrumentolegalresoluciones_descripcion=payload.get("descripcion", ""),
    )
    return {"id": r.id}


@api.put("/resolucion/{id}/", tags=["secretariador"])
def update_resolucion(request, id: int, payload: dict):
    require_auth(request)
    from secretariador.models import InstrumentosLegalesResoluciones

    r = InstrumentosLegalesResoluciones.objects.filter(id=id).first()
    if not r:
        return {"detail": "Not found"}, 404
    for field in ["instrumentolegalresoluciones_tipo", "instrumentolegalresoluciones_numero",
                  "instrumentolegalresoluciones_ano", "instrumentolegalresoluciones_descripcion"]:
        key = field.replace("instrumentolegalresoluciones_", "")
        if key in payload:
            setattr(r, field, payload[key])
    r.save()
    return {"id": r.id}


@api.delete("/resolucion/{id}/", tags=["secretariador"])
def delete_resolucion(request, id: int):
    require_auth(request)
    from secretariador.models import InstrumentosLegalesResoluciones

    deleted, _ = InstrumentosLegalesResoluciones.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Resoluciones Directorio ---
@api.get("/resoluciones-directorio/", tags=["secretariador"])
def list_resoluciones_directorio(request):
    user = require_auth(request)
    from secretariador.models import InstrumentosLegalesResolucionesDirectorio

    qs = InstrumentosLegalesResolucionesDirectorio.objects.all().order_by("-id")
    ano_filter = request.GET.get("ano", "")
    if ano_filter:
        qs = qs.filter(instrumentolegalresolucionesdirectorio_ano=ano_filter)
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": r.id,
            "tipo": r.instrumentolegalresolucionesdirectorio_tipo,
            "numero": r.instrumentolegalresolucionesdirectorio_numero,
            "ano": r.instrumentolegalresolucionesdirectorio_ano,
            "descripcion": r.instrumentolegalresolucionesdirectorio_descripcion,
        }
        for r in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.post("/resoluciones-directorio/", tags=["secretariador"])
def create_resolucion_directorio(request, payload: dict):
    require_auth(request)
    from secretariador.models import InstrumentosLegalesResolucionesDirectorio

    r = InstrumentosLegalesResolucionesDirectorio.objects.create(
        instrumentolegalresolucionesdirectorio_tipo=payload.get("tipo", "D"),
        instrumentolegalresolucionesdirectorio_numero=payload.get("numero", ""),
        instrumentolegalresolucionesdirectorio_ano=payload.get("ano", ""),
        instrumentolegalresolucionesdirectorio_descripcion=payload.get("descripcion", ""),
    )
    return {"id": r.id}


@api.delete("/resolucion-directorio/{id}/", tags=["secretariador"])
def delete_resolucion_directorio(request, id: int):
    require_auth(request)
    from secretariador.models import InstrumentosLegalesResolucionesDirectorio

    deleted, _ = InstrumentosLegalesResolucionesDirectorio.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Decretos ---
@api.get("/decretos/", tags=["secretariador"])
def list_decretos(request):
    user = require_auth(request)
    from secretariador.models import InstrumentosLegalesDecretos

    qs = InstrumentosLegalesDecretos.objects.all().order_by("-id")
    ano_filter = request.GET.get("ano", "")
    if ano_filter:
        qs = qs.filter(instrumentolegaldecretos_ano=ano_filter)
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": d.id,
            "tipo": d.instrumentolegaldecretos_tipo,
            "numero": d.instrumentolegaldecretos_numero,
            "ano": d.instrumentolegaldecretos_ano,
            "descripcion": d.instrumentolegaldecretos_descripcion,
        }
        for d in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/decreto/{id}/", tags=["secretariador"])
def retrieve_decreto(request, id: int):
    require_auth(request)
    from secretariador.models import InstrumentosLegalesDecretos

    d = InstrumentosLegalesDecretos.objects.filter(id=id).first()
    if not d:
        return {"detail": "Not found"}, 404
    return {
        "id": d.id,
        "tipo": d.instrumentolegaldecretos_tipo,
        "numero": d.instrumentolegaldecretos_numero,
        "ano": d.instrumentolegaldecretos_ano,
        "descripcion": d.instrumentolegaldecretos_descripcion,
    }


@api.post("/decretos/", tags=["secretariador"])
def create_decreto(request, payload: dict):
    require_auth(request)
    from secretariador.models import InstrumentosLegalesDecretos

    d = InstrumentosLegalesDecretos.objects.create(
        instrumentolegaldecretos_tipo=payload.get("tipo", "P"),
        instrumentolegaldecretos_numero=payload.get("numero", ""),
        instrumentolegaldecretos_ano=payload.get("ano", ""),
        instrumentolegaldecretos_descripcion=payload.get("descripcion", "Escala de viáticos"),
    )
    return {"id": d.id}


@api.delete("/decreto/{id}/", tags=["secretariador"])
def delete_decreto(request, id: int):
    require_auth(request)
    from secretariador.models import InstrumentosLegalesDecretos

    deleted, _ = InstrumentosLegalesDecretos.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- MontoViaticoDiario ---
@api.get("/montos-viaticos/", tags=["secretariador"])
def list_montos_viaticos(request):
    user = require_auth(request)
    from secretariador.models import MontoViaticoDiario

    qs = MontoViaticoDiario.objects.select_related("montoviaticodiario_decreto_reglamentario").all().order_by("-id")
    decreto_id = request.GET.get("decreto", "")
    if decreto_id:
        qs = qs.filter(montoviaticodiario_decreto_reglamentario_id=decreto_id)
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": mv.id,
            "decreto_id": mv.montoviaticodiario_decreto_reglamentario_id,
            "estrato_uno_interior": float(mv.montoviaticodiario_estrato_uno_interior),
            "estrato_dos_interior": float(mv.montoviaticodiario_estrato_dos_interior),
        }
        for mv in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.post("/montos-viaticos/", tags=["secretariador"])
def create_monto_viatico(request, payload: dict):
    require_auth(request)
    from secretariador.models import MontoViaticoDiario

    mv = MontoViaticoDiario.objects.create(
        montoviaticodiario_decreto_reglamentario_id=payload.get("decreto_id"),
    )
    return {"id": mv.id}


@api.delete("/monto-viatico/{id}/", tags=["secretariador"])
def delete_monto_viatico(request, id: int):
    require_auth(request)
    from secretariador.models import MontoViaticoDiario

    deleted, _ = MontoViaticoDiario.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Comisionado ---
@api.get("/comisionados/", tags=["secretariador"])
def list_comisionados(request):
    user = require_auth(request)
    from secretariador.models import Comisionado

    qs = Comisionado.objects.select_related(
        "comisionado_cargo", "comisionado_cargo_decreto",
        "comisionado_cargo_interno"
    ).all().order_by("comisionado_apellidos")
    search = request.GET.get("q", "").strip()
    if search:
        qs = qs.filter(
            Q(comisionado_nombres__icontains=search) | Q(comisionado_apellidos__icontains=search)
        )
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": c.id,
            "nombres": c.comisionado_nombres,
            "apellidos": c.comisionado_apellidos,
            "dni": float(c.comisionado_dni),
            "cargo_id": c.comisionado_cargo_id,
        }
        for c in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/comisionado/{id}/", tags=["secretariador"])
def retrieve_comisionado(request, id: int):
    require_auth(request)
    from secretariador.models import Comisionado

    c = Comisionado.objects.filter(id=id).first()
    if not c:
        return {"detail": "Not found"}, 404
    return {
        "id": c.id,
        "nombres": c.comisionado_nombres,
        "apellidos": c.comisionado_apellidos,
        "dni": float(c.comisionado_dni),
        "cargo_id": c.comisionado_cargo_id,
    }


@api.post("/comisionados/", tags=["secretariador"])
def create_comisionado(request, payload: dict):
    require_auth(request)
    from secretariador.models import Comisionado

    c = Comisionado.objects.create(
        comisionado_nombres=payload.get("nombres", ""),
        comisionado_apellidos=payload.get("apellidos", ""),
        comisionado_abreviatura=payload.get("abreviatura", "Sr."),
        comisionado_sexo=payload.get("sexo"),
        comisionado_cargo_id=payload.get("cargo_id"),
        comisionado_dni=payload.get("dni"),
        comisionado_cuit=payload.get("cuit"),
    )
    return {"id": c.id, "nombre_y_apellido": c.comisionado_nombreyapellido}


@api.delete("/comisionado/{id}/", tags=["secretariador"])
def delete_comisionado(request, id: int):
    require_auth(request)
    from secretariador.models import Comisionado

    deleted, _ = Comisionado.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Organigrama ---
@api.get("/organigramas/", tags=["secretariador"])
def list_organigramas(request):
    user = require_auth(request)
    from secretariador.models import Organigrama

    qs = Organigrama.objects.all().order_by("id")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": o.id,
            "cargo": o.organigrama_cargo,
            "escalafon": float(o.organigrama_escalafon),
        }
        for o in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.post("/organigramas/", tags=["secretariador"])
def create_organigrama(request, payload: dict):
    require_auth(request)
    from secretariador.models import Organigrama

    o = Organigrama.objects.create(
        organigrama_cargo=payload.get("cargo", ""),
        organigrama_escalafon=payload.get("escalafon", 2),
    )
    return {"id": o.id, "cargo": o.organigrama_cargo}


@api.delete("/organigrama/{id}/", tags=["secretariador"])
def delete_organigrama(request, id: int):
    require_auth(request)
    from secretariador.models import Organigrama

    deleted, _ = Organigrama.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Vehiculo ---
@api.get("/vehiculos/", tags=["secretariador"])
def list_vehiculos(request):
    user = require_auth(request)
    from secretariador.models import Vehiculo

    qs = Vehiculo.objects.select_related(
        "vehiculo_poliza_aseguradora", "vehiculo_titular_agente", "vehiculo_titular_empresa"
    ).all().order_by("id")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": v.id,
            "modelo": v.vehiculo_modelo,
            "patente": v.vehiculo_patente,
            "caracter": v.vehiculo_caracter,
        }
        for v in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.post("/vehiculos/", tags=["secretariador"])
def create_vehiculo(request, payload: dict):
    require_auth(request)
    from secretariador.models import Vehiculo

    v = Vehiculo.objects.create(
        vehiculo_modelo=payload.get("modelo", ""),
        vehiculo_patente=payload.get("patente", ""),
        vehiculo_caracter=payload.get("caracter", "O"),
    )
    return {"id": v.id, "modelo": v.vehiculo_modelo}


@api.delete("/vehiculo/{id}/", tags=["secretariador"])
def delete_vehiculo(request, id: int):
    require_auth(request)
    from secretariador.models import Vehiculo

    deleted, _ = Vehiculo.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Solicitud (complex model with M2M) ---
@api.get("/solicitudes/", tags=["secretariador"])
def list_solicitudes(request):
    user = require_auth(request)
    from secretariador.models import Solicitud

    qs = Solicitud.objects.select_related(
        "solicitud_solicitante", "solicitud_provincia"
    ).all().order_by("-id")
    provincia_id = request.GET.get("provincia", "")
    if provincia_id:
        qs = qs.filter(solicitud_provincia_id=provincia_id)
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": s.id,
            "actuacion": s.solicitud_actuacion,
            "solicitante_id": s.solicitud_solicitante_id,
            "provincia_id": s.solicitud_provincia_id,
            "fecha_desde": str(s.solicitud_fecha_desde),
            "fecha_hasta": str(s.solicitud_fecha_hasta),
        }
        for s in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.get("/solicitud/{id}/", tags=["secretariador"])
def retrieve_solicitud(request, id: int):
    require_auth(request)
    from secretariador.models import Solicitud

    s = Solicitud.objects.filter(id=id).first()
    if not s:
        return {"detail": "Not found"}, 404
    return {
        "id": s.id,
        "actuacion": s.solicitud_actuacion,
        "solicitante_id": s.solicitud_solicitante_id,
        "provincia_id": s.solicitud_provincia_id,
        "fecha_desde": str(s.solicitud_fecha_desde),
        "fecha_hasta": str(s.solicitud_fecha_hasta),
    }


@api.post("/solicitudes/", tags=["secretariador"])
def create_solicitud(request, payload: dict):
    require_auth(request)
    from secretariador.models import Solicitud

    s = Solicitud.objects.create(
        solicitud_solicitante_id=payload.get("solicitante_id"),
        solicitud_provincia_id=payload.get("provincia_id"),
        solicitud_fecha_desde=payload.get("fecha_desde"),
        solicitud_fecha_hasta=payload.get("fecha_hasta"),
        solicitud_tareas=payload.get("tareas", ""),
    )
    return {"id": s.id, "actuacion": s.solicitud_actuacion}


@api.delete("/solicitud/{id}/", tags=["secretariador"])
def delete_solicitud(request, id: int):
    require_auth(request)
    from secretariador.models import Solicitud

    deleted, _ = Solicitud.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- ComisionadoSolicitud ---
@api.get("/comisionados-solicitudes/", tags=["secretariador"])
@get_group_perms("dirgral_usuarios")
def list_comisionados_solicitudes(request):
    user = require_auth(request)
    from secretariador.models import ComisionadoSolicitud

    qs = ComisionadoSolicitud.objects.select_related(
        "comisionadosolicitud_nombre"
    ).all().order_by("-id")
    solicitud_id = request.GET.get("solicitud", "")
    if solicitud_id:
        qs = qs.filter(comisionadosolicitud_foreign_id=solicitud_id)
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": cs.id,
            "solicitud_id": cs.comisionadosolicitud_foreign_id,
            "comisionado_id": cs.comisionadosolicitud_nombre_id,
            "colaborador": cs.comisionadosolicitud_colaborador,
            "chofer": cs.comisionadosolicitud_chofer,
        }
        for cs in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.post("/comisionados-solicitudes/", tags=["secretariador"])
def create_comisionado_solicitud(request, payload: dict):
    require_auth(request)
    from secretariador.models import ComisionadoSolicitud

    cs = ComisionadoSolicitud.objects.create(
        comisionadosolicitud_foreign_id=payload.get("solicitud_id"),
        comisionadosolicitud_nombre_id=payload.get("comisionado_id"),
        comisionadosolicitud_colaborador=payload.get("colaborador", False),
        comisionadosolicitud_chofer=payload.get("chofer", False),
    )
    return {"id": cs.id}


@api.delete("/comisionado-solicitud/{id}/", tags=["secretariador"])
def delete_comisionado_solicitud(request, id: int):
    require_auth(request)
    from secretariador.models import ComisionadoSolicitud

    deleted, _ = ComisionadoSolicitud.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Incorporacion ---
@api.get("/incorporaciones/", tags=["secretariador"])
def list_incorporaciones(request):
    user = require_auth(request)
    from secretariador.models import Incorporacion

    qs = Incorporacion.objects.select_related(
        "incorporacion_solicitud", "incorporacion_solicitante"
    ).all().order_by("-id")
    solicitud_id = request.GET.get("solicitud", "")
    if solicitud_id:
        qs = qs.filter(incorporacion_solicitud_id=solicitud_id)
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {
            "id": i.id,
            "solicitud_id": i.incorporacion_solicitud_id,
            "actuacion": i.incorporacion_actuacion,
        }
        for i in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.post("/incorporaciones/", tags=["secretariador"])
def create_incorporacion(request, payload: dict):
    require_auth(request)
    from secretariador.models import Incorporacion

    i = Incorporacion.objects.create(
        incorporacion_solicitud_id=payload.get("solicitud_id"),
        incorporacion_solicitante_id=payload.get("solicitante_id"),
    )
    return {"id": i.id}


@api.delete("/incorporacion/{id}/", tags=["secretariador"])
def delete_incorporacion(request, id: int):
    require_auth(request)
    from secretariador.models import Incorporacion

    deleted, _ = Incorporacion.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}

