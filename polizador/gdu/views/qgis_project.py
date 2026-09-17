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

# Mismo patrón que UnicodeUsernameValidator de Django (auth.User): evita que un
# username con comilla simple rompa el par key='value' del datasource WFS
# armado en reconectar_wfs.construir_datasource_wfs.
_LDAP_USERNAME_RE = re.compile(r"[\w.@+-]+")


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
    Manager local de QGIS), se usa esa vía rápida en su lugar.

    El usuario de Django logueado no siempre coincide con el usuario LDAP real
    (hay cuentas locales, ver AUTHENTICATION_BACKENDS en settings.py, que no
    pasan por django_auth_ldap.backend.LDAPBackend) -- para esos casos se puede
    pasar ?ldap_username=<usuario de red> y se usa ese en lugar del username de
    Django logueado. Se ignora si se pasa authcfg (misma exclusión mutua que
    ya tiene reconectar_wfs.py entre --authcfg y --username)."""
    if not any(request.user.has_perm(p) for p in PERMISOS_CAPAS):
        raise PermissionDenied

    authcfg = request.GET.get("authcfg", "").strip()
    if authcfg and not _AUTHCFG_RE.fullmatch(authcfg):
        return JsonResponse({"errors": "authcfg inválido: debe tener 7 caracteres alfanuméricos"}, status=400)

    ldap_username = request.GET.get("ldap_username", "").strip()
    if ldap_username and not _LDAP_USERNAME_RE.fullmatch(ldap_username):
        return JsonResponse({"errors": "usuario LDAP inválido"}, status=400)

    contenido = generar_paquete_qgis(ldap_username or request.user.username, authcfg or None)
    return FileResponse(
        io.BytesIO(contenido),
        as_attachment=True,
        filename=f"gdu_qgis_{request.user.username}.zip",
    )
