import io
import re
import zipfile

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.urls import reverse
from django.views.decorators.http import require_GET

from gdu.auditoria import registrar_evento
from gdu.oapif import api

# la raíz OAPIF con la que se generó el proyecto (armar_proyecto.py --url), en cada capa
_URL_OAPIF = re.compile(r"url='[^']*/gdu/oapif/'")
# las acciones "Abrir URL" a páginas de gdu (Generar UF en las parcelas), generadas contra el
# mismo servidor: la base hasta /gdu/ inclusive
_ACCION_URL_GDU = re.compile(r'action="https?://[^"]*?/gdu/')


def proyecto_con_url(contenido, url_oapif):
    """El .qgz con las capas, y las acciones que abren páginas de gdu, apuntando al servidor de
    `url_oapif`. El proyecto versionado se genera contra un servidor puntual (el de
    desarrollo); acá se le cambia la URL sin QGIS, editando el .qgs adentro del zip."""
    url_gdu = url_oapif.removesuffix("oapif/")
    entrada = zipfile.ZipFile(io.BytesIO(contenido))
    salida = io.BytesIO()
    with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as nuevo:
        for item in entrada.infolist():
            datos = entrada.read(item)
            if item.filename.endswith(".qgs"):
                qgs = _URL_OAPIF.sub(f"url='{url_oapif}'", datos.decode())
                datos = _ACCION_URL_GDU.sub(f'action="{url_gdu}', qgs).encode()
            nuevo.writestr(item, datos)
    return salida.getvalue()


@login_required
@require_GET
def descargar_proyecto_qgis(request):
    """
    El proyecto QGIS de GDU (qgis-gdu/oapif/gdu-oapif.qgz), conectado a las capas OGC API -
    Features de este mismo servidor. Es el mismo archivo para todos: guarda solo el id de
    autenticación (gduoapf), que cada usuario carga una vez en su QGIS con su usuario y clave
    (ver qgis-gdu/oapif/README.md). Lo puede bajar quien vea alguna capa OAPIF.
    """
    if not any(coleccion.has_view_permission(request) for coleccion in api.collections.values()):
        raise PermissionDenied
    try:
        contenido = settings.GDU_QGIS_PROYECTO.read_bytes()
    except FileNotFoundError:
        raise Http404("No está el proyecto QGIS en el servidor")
    url_oapif = request.build_absolute_uri(reverse("gdu-oapif:root"))
    registrar_evento(request, "descargaProyectoQgis")
    return FileResponse(
        io.BytesIO(proyecto_con_url(contenido, url_oapif)), as_attachment=True, filename="gdu-oapif.qgz",
    )
