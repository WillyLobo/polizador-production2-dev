# personalizador app API views
from api.router import api
from api.permissions import require_auth


# --- CustomUser ---
@api.get("/users/", tags=["personalizador"])
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


@api.get("/user/{id}/", tags=["personalizador"])
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


# --- Gerencia ---
@api.get("/gerencias/", tags=["personalizador"])
def list_gerencias(request):
    user = require_auth(request)
    from personalizador.models import Gerencia

    qs = Gerencia.objects.all().order_by("id")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {"id": g.id, "nombre": g.gerencia_nombre, "cuof": g.gerencia_cuof}
        for g in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.post("/gerencias/", tags=["personalizador"])
def create_gerencia(request, payload: dict):
    require_auth(request)
    from personalizador.models import Gerencia

    g = Gerencia.objects.create(
        gerencia_nombre=payload.get("nombre", ""),
        gerencia_cuof=payload.get("cuof", ""),
    )
    return {"id": g.id}


@api.delete("/gerencia/{id}/", tags=["personalizador"])
def delete_gerencia(request, id: int):
    require_auth(request)
    from personalizador.models import Gerencia

    deleted, _ = Gerencia.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Direccion ---
@api.get("/direcciones/", tags=["personalizador"])
def list_direcciones(request):
    user = require_auth(request)
    from personalizador.models import Direccion

    qs = Direccion.objects.all().order_by("id")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {"id": d.id, "nombre": d.direccion_nombre, "cuof": d.direccion_cuof}
        for d in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.post("/direcciones/", tags=["personalizador"])
def create_direccion(request, payload: dict):
    require_auth(request)
    from personalizador.models import Direccion

    d = Direccion.objects.create(
        direccion_nombre=payload.get("nombre", ""),
        direccion_cuof=payload.get("cuof", ""),
    )
    return {"id": d.id}


@api.delete("/direccion/{id}/", tags=["personalizador"])
def delete_direccion(request, id: int):
    require_auth(request)
    from personalizador.models import Direccion

    deleted, _ = Direccion.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}


# --- Departamento (personalizador) ---
@api.get("/departamentos-personal/", tags=["personalizador"])
def list_departamentos_personal(request):
    user = require_auth(request)
    from personalizador.models import Departamento

    qs = Departamento.objects.all().order_by("id")
    page = int(request.GET.get("page", 1))
    per_page = min(int(request.GET.get("per_page", 50)), 200)
    start = (page - 1) * per_page
    end = start + per_page
    total = qs.count()
    results = [
        {"id": d.id, "nombre": d.departamento_nombre, "cuof": d.departamento_cuof}
        for d in qs[start:end]
    ]
    return {
        "count": total,
        "next": f"?page={page + 1}&per_page={per_page}" if end < total else None,
        "previous": f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "results": results,
    }


@api.post("/departamentos-personal/", tags=["personalizador"])
def create_departamento_personal(request, payload: dict):
    require_auth(request)
    from personalizador.models import Departamento

    d = Departamento.objects.create(
        departamento_nombre=payload.get("nombre", ""),
        departamento_cuof=payload.get("cuof", ""),
    )
    return {"id": d.id}


@api.delete("/departamento-personal/{id}/", tags=["personalizador"])
def delete_departamento_personal(request, id: int):
    require_auth(request)
    from personalizador.models import Departamento

    deleted, _ = Departamento.objects.filter(id=id).delete()
    return {"deleted": bool(deleted)}
