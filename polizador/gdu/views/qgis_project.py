import io
import re

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, JsonResponse
from django.views.decorators.http import require_GET

from gdu.services.qgis_reconnect import generar_paquete_qgis
from gdu.views.visor import PERMISOS_CAPAS

# Id de una config "Basic" del Auth Manager local de QGIS (Settings > Options >
# Authentication) -- 7 caracteres, no es un secreto (ver reconectar_wfs.py).
_AUTHCFG_RE = re.compile(r"[A-Za-z0-9]{7}")


@login_required
@require_GET
def descargar_proyecto_qgis(request):
    """Descarga un .zip con gdu.qgz (reconectado a WFS en GeoServer) + forms/,
    para abrir en QGIS Desktop. Mismo público que el visor web
    (gdu/views/visor.py::mapa): no hay un permiso propio para esto, la
    autorización real por capa la hace GeoServer
    (geoserver/templates/layers.properties) contra el mismo username.

    Por default reconecta con username=<usuario logueado> (sin password) --
    QGIS pide la contraseña LDAP la primera vez que abre cada capa, lento en
    tablas grandes (ver "Pendiente" en geoserver/INSTALL_PRODUCCION.md). Si se
    pasa ?authcfg=<id de 7 caracteres> (ya cargado por el usuario en su Auth
    Manager local de QGIS), se usa esa vía rápida en su lugar."""
    if not any(request.user.has_perm(p) for p in PERMISOS_CAPAS):
        raise PermissionDenied

    authcfg = request.GET.get("authcfg", "").strip()
    if authcfg and not _AUTHCFG_RE.fullmatch(authcfg):
        return JsonResponse({"errors": "authcfg inválido: debe tener 7 caracteres alfanuméricos"}, status=400)

    contenido = generar_paquete_qgis(request.user.username, authcfg or None)
    return FileResponse(
        io.BytesIO(contenido),
        as_attachment=True,
        filename=f"gdu_qgis_{request.user.username}.zip",
    )
