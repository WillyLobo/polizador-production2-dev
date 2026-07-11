import re

import smbclient
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET

# ej: "20-107-86/subdivision" (tal cual viven en visualizador.viviendas.planos,
# separados por ", " cuando una vivienda tiene varios). El sufijo "/subdivision"
# (o cualquier otro texto) después del año se descarta, igual que hacía el
# parseInt tolerante del original en JS.
_ANO_LIDER_DIGITOS = re.compile(r"^(\d+)")


@login_required
@require_GET
def plano(request):
    """
    Equivalente a controllers/smb.js::plano. Lee un JPG escaneado desde el recurso
    SMB de planos digitales. No se pudo probar contra el servidor real (10.106.16.14)
    desde este entorno de desarrollo, solo se validó que arma la ruta/llama a la
    librería correctamente.

    Recibe el identificador de plano por query string (`?plano=...`) en vez de
    como segmento de URL: los valores reales (columna `visualizador.viviendas.planos`)
    traen una "/" (p.ej. "20-107-86/subdivision"), que el path converter `str` de
    Django no puede matchear como un único segmento.
    """
    plano = request.GET.get("plano", "")
    partes = plano.split("-")
    if len(partes) != 3:
        return JsonResponse({"errors": "formato de plano inválido, se espera carpeta-nro-ano"}, status=400)

    ano_match = _ANO_LIDER_DIGITOS.match(partes[2])
    if not ano_match:
        return JsonResponse({"errors": "formato de plano inválido"}, status=400)

    try:
        carpeta = int(partes[0])
        nro_plano = partes[1]
        ano_plano = ano_match.group(1).zfill(2)
    except ValueError:
        return JsonResponse({"errors": "formato de plano inválido"}, status=400)

    archivo = f"{carpeta}\\{carpeta}-{nro_plano}-{ano_plano}.jpg"
    share = settings.GDU_SMB_SHARE  # \\10.106.16.14\planos digitales
    servidor = share.strip("\\").split("\\")[0]
    ruta_completa = f"{share}\\{archivo}"

    try:
        smbclient.register_session(
            servidor,
            username=f"{settings.GDU_SMB_DOMAIN}\\{settings.GDU_SMB_USERNAME}",
            password=settings.GDU_SMB_PASSWORD,
        )
        with smbclient.open_file(ruta_completa, mode="rb") as f:
            contenido = f.read()
    except Exception:
        return JsonResponse({"errors": "No se encontró el plano"}, status=404)

    return HttpResponse(contenido, content_type="image/jpeg")
