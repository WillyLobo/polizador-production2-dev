import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_POST

TOKEN_CACHE_KEY = "gdu:3450:token"
TOKEN_CACHE_TIMEOUT = 60 * 30  # el token de la API externa expira; 30 min es conservador


def _login():
    resp = requests.post(
        f"{settings.GDU_3450_API_BASE_URL}/oauth/access_token",
        data={
            "username": settings.GDU_3450_API_USERNAME,
            "password": settings.GDU_3450_API_PASSWORD,
            "client_id": settings.GDU_3450_API_CLIENT_ID,
            "grant_type": "password",
        },
        timeout=15,
    )
    resp.raise_for_status()
    token = resp.json().get("access_token")
    cache.set(TOKEN_CACHE_KEY, token, timeout=TOKEN_CACHE_TIMEOUT)
    return token


def _consultar(nro_adjudicatario, token, reintentar=True):
    resp = requests.post(
        f"{settings.GDU_3450_API_BASE_URL}/rest/wsIpduvAdjuGIS",
        json={"DCAdjudicatario": nro_adjudicatario},
        headers={"Authorization": token},
        timeout=15,
    )
    if resp.status_code == 401 and reintentar:
        nuevo_token = _login()
        return _consultar(nro_adjudicatario, nuevo_token, reintentar=False)
    resp.raise_for_status()
    return resp.json()


@login_required
@require_POST
def consultar_3450(request):
    """Equivalente a controllers/3450.js::s3450."""
    nro_adjudicatario = request.POST.get("nro_adjudicatario")
    if not nro_adjudicatario:
        return JsonResponse({"errors": "nro_adjudicatario is not valid"}, status=400)

    token = cache.get(TOKEN_CACHE_KEY)
    try:
        if not token:
            token = _login()
        data = _consultar(nro_adjudicatario, token)
    except requests.RequestException:
        return JsonResponse({"error": "error desconocido"}, status=500)

    return JsonResponse(data, safe=False)
