"""
Genera, en memoria, una copia de qgis-gdu/gdu.qgz con las capas de
settings.GDU_WFS_LAYERS reconectadas a WFS en GeoServer con el username del
usuario de Django/LDAP que pide la descarga (ver gdu/views/qgis_project.py).

No reimplementa la reescritura del XML: carga qgis-gdu/scripts/reconectar_wfs.py
como módulo (mismo truco de importlib que ese script ya usa para
forms/layer_config.py) para que el CLI manual y esta vista compartan una única
fuente de verdad, ya validada a mano contra QGIS Desktop (ver qgis-gdu/README.md).
"""
import importlib.util
import io
import tempfile
import zipfile
from pathlib import Path

from django.conf import settings


def _cargar_reconectar_wfs():
    script_path = settings.QGIS_GDU_DIR / "scripts" / "reconectar_wfs.py"
    spec = importlib.util.spec_from_file_location("reconectar_wfs", script_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


reconectar_wfs = _cargar_reconectar_wfs()


def generar_qgz_personalizado(username: str, authcfg: str | None = None) -> bytes:
    """Devuelve los bytes del .qgz de qgis-gdu/gdu.qgz con settings.GDU_WFS_LAYERS
    reconectadas a WFS.

    Sin authcfg (default): embebe username=<username> sin password -- GeoServer
    en mode=CHALLENGE hace que QGIS pida la contraseña LDAP real al abrir cada
    capa la primera vez. Con authcfg: embebe authcfg='<authcfg>' en vez de
    username, replicando la exclusión mutua del propio CLI de reconectar_wfs.py
    (--authcfg vs --username/--password) -- ver "Pendiente" en
    geoserver/INSTALL_PRODUCCION.md sobre por qué username-only es lento/inestable
    en tablas grandes y authcfg es la vía rápida (requiere que el usuario ya haya
    cargado esa config "Basic" en su Auth Manager local de QGIS).

    No usa --solo-esta-capa: se conserva el proyecto completo, igual que el
    flujo manual documentado en INSTALL_PRODUCCION.md."""
    forms_dir = settings.QGIS_GDU_DIR / "forms"
    config = reconectar_wfs.cargar_layer_config(forms_dir)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        with zipfile.ZipFile(settings.QGIS_GDU_DIR / "gdu.qgz") as zin:
            zin.extractall(tmp)

        qgs_candidates = list(tmp.glob("*.qgs"))
        if len(qgs_candidates) != 1:
            raise RuntimeError(
                f"Se esperaba un único .qgs dentro de gdu.qgz, se encontraron {len(qgs_candidates)}"
            )
        qgs_path = qgs_candidates[0]
        qgs_text = qgs_path.read_text(encoding="utf-8")

        for layer in settings.GDU_WFS_LAYERS:
            if layer not in config:
                raise RuntimeError(f"'{layer}' (GDU_WFS_LAYERS) no está en layer_config.py")
            layer_id = config[layer]["id"]
            datasource_wfs = reconectar_wfs.construir_datasource_wfs(
                settings.GDU_GEOSERVER_URL, "gdu", layer, settings.GDU_WFS_SRS, "auto",
                None if authcfg else username, None, authcfg,
            )
            reconectar_wfs.verificar_estructura(qgs_text, layer_id)
            qgs_text, encontrado_maplayer, _ = reconectar_wfs.reconectar_texto(qgs_text, layer_id, datasource_wfs)
            if not encontrado_maplayer:
                raise RuntimeError(f"No se pudo reconectar la capa '{layer}' (id={layer_id}) a WFS")

        qgs_path.write_text(qgs_text, encoding="utf-8")

        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zout:
            for f in tmp.iterdir():
                zout.write(f, f.name)
        return buffer.getvalue()


def generar_paquete_qgis(username: str, authcfg: str | None = None) -> bytes:
    """Zip final para descargar: el .qgz personalizado (generar_qgz_personalizado)
    más qgis-gdu/forms/ (los .ui referenciados por ruta relativa "./forms/..." desde
    el .qgz -- sin ellos QGIS falla con NameError al abrir el proyecto). El nombre
    del .qgz dentro del zip sigue basado en el username de Django (para identificar
    de quién es el archivo) aunque la conexión interna use authcfg."""
    qgz_bytes = generar_qgz_personalizado(username, authcfg)
    forms_dir = settings.QGIS_GDU_DIR / "forms"

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zout:
        zout.writestr(f"gdu.wfs.{username}.qgz", qgz_bytes)
        for f in forms_dir.rglob("*"):
            if f.is_file() and "__pycache__" not in f.parts:
                zout.write(f, str(Path("forms") / f.relative_to(forms_dir)))
    return buffer.getvalue()
