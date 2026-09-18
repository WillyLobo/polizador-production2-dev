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
import re
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
    reconectadas a WFS, y el resto del proyecto (~180 capas Postgres directas,
    la mayoría apuntando a la base de producción, no alcanzable desde afuera --
    ver "Pendiente" en geoserver/INSTALL_PRODUCCION.md) eliminado -- equivalente
    a correr reconectar_wfs.py con --solo-esta-capa. Servidor de prueba: no hay
    todavía dónde repartir el proyecto completo, así que no tiene sentido que
    QGIS intente (y quede colgado con timeouts) conectarse a esas capas.

    Sin authcfg (default): embebe username=<username> sin password -- GeoServer
    en mode=CHALLENGE hace que QGIS pida la contraseña LDAP real al abrir cada
    capa la primera vez. Con authcfg: embebe authcfg='<authcfg>' en vez de
    username, replicando la exclusión mutua del propio CLI de reconectar_wfs.py
    (--authcfg vs --username/--password) -- ver "Pendiente" en
    geoserver/INSTALL_PRODUCCION.md sobre por qué username-only es lento/inestable
    en tablas grandes y authcfg es la vía rápida (requiere que el usuario ya haya
    cargado esa config "Basic" en su Auth Manager local de QGIS)."""
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

        # datasources: nombre de entidad -> datasource WFS ya construido, para
        # TODAS las capas reconectadas (principales + de soporte) -- se usa
        # también más abajo para arreglar los <Option
        # name="ReferencedLayerDataSource"> que otras capas guardan en caché.
        datasources = {}

        layer_ids = {}
        for layer in settings.GDU_WFS_LAYERS:
            if layer not in config:
                raise RuntimeError(f"'{layer}' (GDU_WFS_LAYERS) no está en layer_config.py")
            layer_id = config[layer]["id"]
            layer_ids[layer] = layer_id
            datasource_wfs = reconectar_wfs.construir_datasource_wfs(
                settings.GDU_GEOSERVER_URL, "gdu", layer, settings.GDU_WFS_SRS, "auto",
                None if authcfg else username, None, authcfg,
            )
            datasources[layer] = datasource_wfs
            reconectar_wfs.verificar_estructura(qgs_text, layer_id)
            qgs_text, encontrado_maplayer, _ = reconectar_wfs.reconectar_texto(qgs_text, layer_id, datasource_wfs)
            if not encontrado_maplayer:
                raise RuntimeError(f"No se pudo reconectar la capa '{layer}' (id={layer_id}) a WFS")

        # Cierre de dependencias (capas de soporte, ej. las que dependen de
        # 'intervencion': tipo_estado, programa, etc. -- lookups de sus propios
        # campos FK) -- van a WFS igual que las principales, no a Postgres
        # directo: así no hace falta repartir una credencial de Postgres
        # compartida (no por usuario, sin las Data Access Rules de GeoServer)
        # solo para poder ver esos combos. Deben estar publicadas en GeoServer
        # (GS_FEATURETYPES en geoserver/deploy_geoserver.sh) o esto falla.
        cierre = reconectar_wfs.calcular_cierre_dependencias(qgs_text, set(layer_ids.values()))
        capas_soporte = cierre - set(layer_ids.values())
        id_a_nombre = {v["id"]: k for k, v in config.items()}

        # gdu.qgz tiene capas "bookmark" duplicadas -- ej. 'Región_10'/
        # 'Resistencia_Norte/Sur/Este' son 4 instancias separadas de
        # catastro.parcela, cada una pre-filtrada por departamento con su
        # propio sql=ST_Intersects(...) y su propio <maplayer> id, pero
        # comparten las MISMAS <relation> (mismo nombre, generado por QGIS
        # desde el constraint real de la tabla) que la capa real 'parcela' --
        # indistinguibles para calcular_cierre_dependencias, que las arrastra
        # igual que a 'parcela' apenas algo se relaciona con ellas. GeoServer
        # solo publica una capa 'parcela', no 4 típenames por departamento, así
        # que reconectarlas todas a WFS revienta con un típename inexistente
        # para 3 de las 4. Se reconecta solo la instancia "canónica" (su alias
        # en layer_config.py coincide con el nombre real de la tabla); las
        # demás se excluyen del proyecto entero (dejar_solo_estas_capas más
        # abajo, vía `cierre`) en vez de dejarlas con su conexión Postgres
        # vieja rota (inalcanzable igual, y confunde con un ícono de capa
        # rota permanente).
        capas_por_tabla: dict[tuple[str, str] | None, list[str]] = {}
        for lid in capas_soporte:
            capas_por_tabla.setdefault(reconectar_wfs.tabla_postgres_de(qgs_text, lid), []).append(lid)
        capas_duplicadas = set()
        for tabla, lids in capas_por_tabla.items():
            if tabla is None or len(lids) == 1:
                continue
            canonica = next((l for l in lids if id_a_nombre.get(l) == tabla[1]), sorted(lids)[0])
            capas_duplicadas.update(l for l in lids if l != canonica)
        if capas_duplicadas:
            cierre -= capas_duplicadas
            capas_soporte -= capas_duplicadas

        for lid in capas_soporte:
            nombre = id_a_nombre.get(lid, lid)
            datasource_wfs = reconectar_wfs.construir_datasource_wfs(
                settings.GDU_GEOSERVER_URL, "gdu", nombre, settings.GDU_WFS_SRS, "auto",
                None if authcfg else username, None, authcfg,
            )
            datasources[nombre] = datasource_wfs
            reconectar_wfs.verificar_estructura(qgs_text, lid)
            qgs_text, encontrado_maplayer, _ = reconectar_wfs.reconectar_texto(qgs_text, lid, datasource_wfs)
            if not encontrado_maplayer:
                raise RuntimeError(f"No se pudo reconectar la capa de soporte '{nombre}' (id={lid}) a WFS")

        requeridas_geom = set(layer_ids.values()) & reconectar_wfs.ids_con_geometria(qgs_text)
        qgs_text = reconectar_wfs.dejar_solo_estas_capas(qgs_text, cierre, requeridas_en_todas_lados=requeridas_geom)

        # reconectar_texto solo reescribe el <maplayer>/<layer-tree-layer> propio
        # de cada capa -- no las copias que OTRAS capas guardan de su datasource
        # viejo (Postgres) en <Option name="ReferencedLayerDataSource"> (cache
        # que usan sus combos de widget de relación). Se reescriben acá aparte,
        # matcheando por el nombre de tabla Postgres original de CUALQUIER capa
        # reconectada (principal o de soporte) -- no hace falta que el valor
        # cacheado sea idéntico al datasource real, solo que no quede
        # apuntando a una conexión vieja.
        def _reescribir_referenced_layer_datasource(m):
            valor = m.group(1)
            for nombre, datasource_wfs in datasources.items():
                if f'table=&quot;public&quot;.&quot;{nombre}&quot;' in valor:
                    nuevo = reconectar_wfs.xml_escape_attr(datasource_wfs)
                    return f'<Option name="ReferencedLayerDataSource" type="QString" value="{nuevo}"'
            return m.group(0)

        qgs_text = re.sub(
            r'<Option name="ReferencedLayerDataSource" type="QString" value="([^"]*)"',
            _reescribir_referenced_layer_datasource, qgs_text,
        )

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
