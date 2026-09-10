#!/usr/bin/env python3
"""
Reescribe una o más capas del proyecto QGIS (por default, `localidad`) de una
conexión Postgres directa a un datasource WFS apuntando a la capa publicada
en GeoServer, sin tocar ninguna otra capa del proyecto ni los formularios/
`nn.py`/`layer_config.py`.

Equivalente al `reconectar_bd.py` de un trabajo previo (recuperado de los .pyc
que quedaron en __pycache__ tras un reset del repo -- ver el propio historial de
este archivo), pero para WFS en vez de Postgres, y deliberadamente escribiendo
solo las capas pedidas por `--layers`, no las ~183 del proyecto (Fase 4a:
generaliza a varias capas a la vez, seguía siendo un solo `--layer` fijo en la
Fase 3). Ese script viejo reconectaba todas las capas Postgres a otro
host/schema y las dejaba de solo lectura (era una herramienta de revisión de
datos); este es al revés a propósito: el punto del plan es que las capas
piloto queden editables vía WFS-T, no de solo lectura.

Toca dos lugares del XML del proyecto por cada capa (los únicos que importan;
se comprobó a mano contra gdu.qgs que ningún Option ReferencedLayerDataSource
--usado por widgets de relación en OTRAS capas-- embebe una copia del
datasource de ninguna de las capas piloto, así que no hace falta tocarlos):
  1. <maplayer>...<datasource> y <maplayer>...<provider> (el layer en sí).
  2. <layer-tree-layer source=... providerKey=...> (la entrada del panel de capas).

El id interno de cada capa (ej. 'localidad_2cb926e9_...') se lee de
forms/layer_config.py (LayerConfig.config[layer]['id']), no se hardcodea acá,
para no poder desincronizarse de la fuente de verdad real.
"""
import argparse
import importlib.util
import re
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape_text, unescape as xml_unescape_text

SCRIPT_DIR = Path(__file__).resolve().parent
QGIS_GDU_DIR = SCRIPT_DIR.parent


def cargar_layer_config(forms_dir: Path):
    spec = importlib.util.spec_from_file_location("layer_config", forms_dir / "layer_config.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LayerConfig.config


def construir_datasource_wfs(geoserver_url: str, workspace: str, layer: str, srs: str,
                              wfs_version: str, username: str | None, password: str | None) -> str:
    url = f"{geoserver_url.rstrip('/')}/{workspace}/wfs"
    partes = [
        "pagingEnabled='true'",
        "preferCoordinatesForWfsT11='false'",
        "restrictToRequestBBOX='1'",
        f"srsname='{srs}'",
        f"typename='{workspace}:{layer}'",
        f"url='{url}'",
        f"version='{wfs_version}'",
    ]
    if username:
        partes.append(f"username='{username}'")
    if password:
        partes.append(f"password='{password}'")
    return " ".join(partes)


def xml_escape_attr(texto: str) -> str:
    return xml_escape_text(texto, {'"': "&quot;"})


def xml_unescape_attr(texto: str) -> str:
    return xml_unescape_text(texto, {"&quot;": '"'})


def bloque_maplayer(qgs_text: str, layer_id: str) -> tuple[int, int, str]:
    """Devuelve (inicio, fin, texto) del <maplayer>...</maplayer> de layer_id."""
    marker = f"<id>{layer_id}</id>"
    idx = qgs_text.index(marker)
    start = qgs_text.rindex("<maplayer", 0, idx)
    end = qgs_text.index("</maplayer>", idx) + len("</maplayer>")
    return start, end, qgs_text[start:end]


def relaciones_por_capa(qgs_text: str) -> dict:
    """referencingLayer -> {referencedLayer, ...}, desde la sección global
    <relations> del proyecto.

    Se probaron y descartaron dos enfoques más específicos, por widget de
    formulario (ver historial de este archivo): el viejo `ReferencedLayerId`
    embebido en <fieldConfiguration>, y una variante más nueva que solo
    guarda el id de una <relation> (Option name="Relation"). Un tercer caso
    (spike N:N, 2026-09-10: el campo "Res. Adjudicación" de Intervención)
    usa un QgsRelationReferenceWidget insertado directo en el .ui **sin
    ninguna config**, que QGIS resuelve en tiempo real contra <relations>
    por nombre de campo -- invisible para los dos enfoques anteriores. Los
    tres estilos, en el fondo, dependen de que exista una <relation> real
    entre las dos capas -- así que alcanza (y es más simple/robusto) con
    mirar <relations> directo: cualquier <relation> donde esta capa sea
    referencingLayer es una dependencia potencial de algún widget de su
    formulario, sea cual sea el estilo que use."""
    m = re.search(r"<relations\b[^>]*>(.*?)</relations>", qgs_text, re.S)
    if not m:
        return {}
    out = {}
    for rel in re.findall(r"<relation\b.*?</relation>", m.group(1), re.S):
        por = re.search(r'referencingLayer="([^"]+)"', rel)
        do = re.search(r'referencedLayer="([^"]+)"', rel)
        if por and do:
            out.setdefault(por.group(1), set()).add(do.group(1))
    return out


def calcular_cierre_dependencias(qgs_text: str, layer_ids: set) -> set:
    """BFS sobre relaciones_por_capa, partiendo de layer_ids, hasta el cierre
    transitivo completo (ej. si A depende de B y B depende de C, el cierre
    incluye A, B y C)."""
    relaciones = relaciones_por_capa(qgs_text)
    cierre = set(layer_ids)
    por_visitar = list(layer_ids)
    while por_visitar:
        lid = por_visitar.pop()
        for dep in relaciones.get(lid, ()):
            if dep not in cierre:
                cierre.add(dep)
                por_visitar.append(dep)
    return cierre


def ids_con_geometria(qgs_text: str) -> set:
    """Ids de capas que tienen geometría propia, según <layerorder> (orden de
    DIBUJO -- por construcción, solo lo tienen las capas con geometría; ver
    también el comentario de dejar_solo_estas_capas). Se usa para saber, entre
    las capas pedidas por --layers, cuáles son "de soporte sin geometría"
    (ej. intervencion/inspector/ejecutor, spike N:N) que --como cualquier
    capa de soporte-- no tienen por qué tener entrada en
    <custom-order>/<legend>/<layerorder> -- antes de esto, pasar una entidad
    sin geometría en --layers rompía con 'faltan capa(s) requerida(s)' ahí,
    porque se asumía que TODO lo pedido en --layers tenía geometría (cierto
    hasta que el spike de intervencion/inspector/ejecutor lo desmintió)."""
    m = re.search(r"<layerorder\b[^>]*>", qgs_text)
    if not m:
        return set()
    cierre_idx = qgs_text.index("</layerorder>", m.end())
    contenido = qgs_text[m.end():cierre_idx]
    return set(re.findall(r'<layer id="([^"]*)"/>', contenido))


DSN_RE = re.compile(r"dbname='[^']*' host=\S+ port=\d+")


def reconectar_postgres_texto(qgs_text: str, layer_id: str, pg_host: str, pg_port: str,
                               pg_dbname: str, pg_schema: str):
    """Para capas 'de soporte' (solo necesarias por un widget de relación de
    otra capa, no pedidas en --layers): en vez de eliminarlas o pasarlas a
    WFS, reescribe su conexión Postgres para que apunten al mismo Postgres
    del piloto (dbname/host/port) y al schema `catastro` en vez de `public`
    -- mismo espíritu que el reconectar_bd.py viejo (host/schema nuevo,
    solo lectura en la práctica ya que no están en --layers), pero acá
    resuelto con re.sub en vez de ElementTree por la misma razón que
    reconectar_texto (ver su docstring). NO toca <provider> (sigue siendo
    "postgres", no WFS). Devuelve (texto_nuevo, encontrado).
    """
    start, end, block = bloque_maplayer(qgs_text, layer_id)

    def _reescribir(texto: str) -> tuple[str, int]:
        nuevo, n = DSN_RE.subn(
            f"dbname='{pg_dbname}' host={pg_host} port={pg_port}", texto, count=1,
        )
        nuevo, n2 = re.subn(r'table="public"\.', f'table="{pg_schema}".', nuevo, count=1)
        return nuevo, (1 if (n and n2) else 0)

    # <datasource> es contenido de texto, no un atributo -- las comillas van
    # literales (sin &quot;), no hace falta unescapar antes de reescribir.
    block, n_ds = re.subn(
        r"<datasource>(.*?)</datasource>",
        lambda m: f"<datasource>{xml_escape_text(_reescribir(m.group(1))[0])}</datasource>",
        block, count=1, flags=re.S,
    )
    encontrado_maplayer = n_ds == 1
    qgs_text = qgs_text[:start] + block + qgs_text[end:]

    ltl_pattern = re.compile(r'<layer-tree-layer[^>]*\bid="%s"[^>]*>' % re.escape(layer_id))
    m = ltl_pattern.search(qgs_text)
    encontrado_layer_tree = False
    if m:
        tag = m.group(0)

        def _reescribir_attr(mm):
            # acá sí es un atributo -- las comillas SÍ vienen como &quot;.
            valor = xml_unescape_attr(mm.group(1))
            nuevo, _ = _reescribir(valor)
            return f'source="{xml_escape_attr(nuevo)}"'

        tag, n1 = re.subn(r'source="([^"]*)"', _reescribir_attr, tag, count=1)
        if n1 == 1:
            qgs_text = qgs_text[:m.start()] + tag + qgs_text[m.end():]
            encontrado_layer_tree = True

    return qgs_text, encontrado_maplayer, encontrado_layer_tree


def verificar_estructura(qgs_text: str, layer_id: str):
    """Falla rápido y claro si los supuestos sobre la forma del XML no se cumplen,
    en vez de dejar que un ET.parse (usado solo para chequear, nunca para
    reescribir el archivo entero -- ver comentario más abajo) tire un error críptico."""
    ET.fromstring(qgs_text)  # valida que sigue siendo XML bien formado antes de tocar nada
    if qgs_text.count(f"<id>{layer_id}</id>") != 1:
        raise RuntimeError(f"se esperaba exactamente un <id>{layer_id}</id>, no se cumple -- abortando")


def reconectar_texto(qgs_text: str, layer_id: str, datasource_wfs: str):
    """Reescribe el <maplayer> y el <layer-tree-layer> de layer_id, a nivel de texto,
    NO parseando+reserializando el documento entero con ElementTree: se probó esa vía
    primero y el round-trip de ET pierde el <!DOCTYPE ...> del proyecto y reformatea
    miles de tags vacíos (<tag/> -> <tag />) en TODO el archivo de 7MB, aunque
    funcionalmente sea XML equivalente -- demasiado ruido para confiar en un diff y
    un cambio de formato que no hace falta para lo que este script necesita tocar.
    Acá ET sólo se usa para validar (ver verificar_estructura), nunca para escribir.

    Devuelve (texto_nuevo, encontrado_maplayer, encontrado_layer_tree).
    """
    marker = f"<id>{layer_id}</id>"
    idx = qgs_text.index(marker)
    start = qgs_text.rindex("<maplayer", 0, idx)
    end = qgs_text.index("</maplayer>", idx) + len("</maplayer>")
    block = qgs_text[start:end]

    block, n_ds = re.subn(
        r"<datasource>.*?</datasource>",
        f"<datasource>{xml_escape_text(datasource_wfs)}</datasource>",
        block, count=1, flags=re.S,
    )
    block, n_prov = re.subn(
        r"<provider([^>]*)>.*?</provider>",
        r"<provider\1>WFS</provider>",
        block, count=1, flags=re.S,
    )
    encontrado_maplayer = (n_ds == 1 and n_prov == 1)
    qgs_text = qgs_text[:start] + block + qgs_text[end:]

    ltl_pattern = re.compile(r'<layer-tree-layer[^>]*\bid="%s"[^>]*>' % re.escape(layer_id))
    m = ltl_pattern.search(qgs_text)
    encontrado_layer_tree = False
    if m:
        tag = m.group(0)
        tag, n1 = re.subn(r'source="[^"]*"', f'source="{xml_escape_attr(datasource_wfs)}"', tag, count=1)
        tag, n2 = re.subn(r'providerKey="[^"]*"', 'providerKey="WFS"', tag, count=1)
        if n1 == 1 and n2 == 1:
            qgs_text = qgs_text[:m.start()] + tag + qgs_text[m.end():]
            encontrado_layer_tree = True

    return qgs_text, encontrado_maplayer, encontrado_layer_tree


def _filtrar_bloques(contenido: str, patron_bloque: str, patron_id, layer_ids: set):
    """Recorre todos los bloques que matchean patron_bloque (regex con re.S) y se queda
    solo con los que contienen alguno de layer_ids según patron_id (regex con un grupo
    de captura). Devuelve (contenido_filtrado, ids_encontrados)."""
    encontrados = set()

    def filtro(m):
        bloque = m.group(0)
        idm = patron_id.search(bloque)
        if idm and idm.group(1) in layer_ids:
            encontrados.add(idm.group(1))
            return bloque
        return ""

    nuevo = re.sub(patron_bloque, filtro, contenido, flags=re.S)
    return nuevo, encontrados


def _indice_cierre_balanceado(text: str, pos_despues_apertura: int, tag: str) -> int:
    """Para tags que pueden anidarse a sí mismos (ej. <layer-tree-group> contiene
    subgrupos que también son <layer-tree-group>, uno por carpeta del panel de
    capas), devuelve el índice de INICIO del </tag> que realmente cierra la
    apertura ubicada antes de pos_despues_apertura, contando profundidad -- un
    simple text.index("</tag>", ...) agarraría el cierre del primer subgrupo
    anidado, no el de la apertura raíz (se detectó así, con --solo-esta-capa
    tirando 'se conservaron 0' porque el recorte de <layer-tree-group> estaba
    truncado antes de llegar a la mayoría de las capas)."""
    apertura_re = re.compile(rf"<{tag}\b[^>]*(?<!/)>")
    cierre = f"</{tag}>"
    depth = 1
    pos = pos_despues_apertura
    while True:
        next_open_m = apertura_re.search(text, pos)
        next_close_idx = text.find(cierre, pos)
        if next_close_idx == -1:
            raise RuntimeError(f"no se encontraron suficientes </{tag}> -- estructura inesperada")
        if next_open_m and next_open_m.start() < next_close_idx:
            depth += 1
            pos = next_open_m.end()
        else:
            depth -= 1
            if depth == 0:
                return next_close_idx
            pos = next_close_idx + len(cierre)


def dejar_solo_estas_capas(qgs_text: str, layer_ids: set, requeridas_en_todas_lados: set = None) -> str:
    """Poda TODAS las demás capas del proyecto (maplayer, layer-tree-layer, legend,
    layerorder, custom-order, relations) para armar una copia de prueba liviana que
    no se cuelgue intentando conectar a las ~180 capas Postgres restantes (que no
    tienen por qué ser alcanzables desde la red donde se prueba QGIS). Separado de
    reconectar_texto a propósito: esto es una conveniencia para probar, no algo que
    el proyecto de referencia (ni el gdu.qgz "completo" reconectado) necesite.

    layer_ids es el cierre completo (capas WFS-T pedidas + de soporte, ver
    calcular_cierre_dependencias) -- se filtra por ese set en TODAS las
    secciones. Pero no todas las secciones tienen entrada para TODAS las
    capas: <custom-order>/<legend>/<layerorder> son listas de ORDEN DE DIBUJO,
    y una capa de soporte sin geometría (ej. 'intervención', agregada solo
    para que ande el combo de un widget de relación) nunca tiene posición ahí
    -- exigir que aparezcan las 6 en esas 3 secciones rompía con "se
    conservaron 4" apenas se sumó la primera capa de soporte sin geometría.
    requeridas_en_todas_lados (default: layer_ids, o sea estricto en todos
    lados si no se pasa nada) son las que SÍ tienen que aparecer siempre --
    <layer-tree-group> y <projectlayers> siguen exigiendo el cierre completo.
    """
    requeridas = requeridas_en_todas_lados if requeridas_en_todas_lados is not None else layer_ids

    def podar_seccion(text, apertura_re, cierre, patron_bloque, patron_id, nombre, anidable=False, requeridas=requeridas):
        m = re.search(apertura_re, text)
        if not m:
            raise RuntimeError(f"no se encontró la sección <{nombre}> -- estructura de proyecto inesperada")
        if anidable:
            cierre_idx = _indice_cierre_balanceado(text, m.end(), nombre)
        else:
            cierre_idx = text.index(cierre, m.end())
        contenido = text[m.end():cierre_idx]
        contenido_filtrado, encontrados = _filtrar_bloques(contenido, patron_bloque, patron_id, layer_ids)
        faltan = requeridas - encontrados
        if faltan:
            raise RuntimeError(f"en <{nombre}> faltan {len(faltan)} capa(s) requerida(s): {faltan} -- abortando")
        return text[:m.end()] + contenido_filtrado + text[cierre_idx:]

    # <layer-tree-group> se anida en sí mismo (una carpeta por grupo del panel de
    # capas) -- por eso anidable=True acá y en ningún otro lado (el resto de las
    # secciones no se contienen a sí mismas, confirmado a mano contra gdu.qgs).
    # Todas las capas (con o sin geometría) aparecen en el panel de capas, así
    # que acá sí se exige el cierre completo (requeridas=layer_ids).
    qgs_text = podar_seccion(
        qgs_text, r"<layer-tree-group\b[^>]*>", "</layer-tree-group>",
        r"<layer-tree-layer\b.*?</layer-tree-layer>", re.compile(r'\bid="([^"]+)"'),
        "layer-tree-group", anidable=True, requeridas=layer_ids,
    )
    # <custom-order> vive DENTRO de <layer-tree-group> (guarda un orden de dibujo
    # alternativo, item por item) -- se poda aparte porque usa <item>id</item>, no
    # <layer-tree-layer>. Está deshabilitado en el proyecto (enabled="0"). Solo
    # trae capas CON geometría (orden de DIBUJO) -- ver docstring, no exigir el
    # cierre completo acá.
    m_co = re.search(r"<custom-order\b[^>]*>", qgs_text)
    if m_co:
        cierre_idx = qgs_text.index("</custom-order>", m_co.end())
        contenido = qgs_text[m_co.end():cierre_idx]
        contenido_filtrado, encontrados = _filtrar_bloques(
            contenido, r"<item>[^<]*</item>", re.compile(r"<item>([^<]*)</item>"), layer_ids,
        )
        faltan = requeridas - encontrados
        if faltan:
            raise RuntimeError(f"en <custom-order> faltan {len(faltan)} capa(s) requerida(s): {faltan}")
        qgs_text = qgs_text[:m_co.end()] + contenido_filtrado + qgs_text[cierre_idx:]

    qgs_text = podar_seccion(
        qgs_text, r"<projectlayers\b[^>]*>", "</projectlayers>",
        r"<maplayer\b.*?</maplayer>", re.compile(r"<id>([^<]+)</id>"),
        "projectlayers", requeridas=layer_ids,
    )
    # <legend>/<layerorder>: mismo caso que <custom-order>, no toda capa sin
    # geometría tiene entrada.
    qgs_text = podar_seccion(
        qgs_text, r"<legend\b[^>]*>", "</legend>",
        r"<legendlayer\b.*?</legendlayer>", re.compile(r'\blayerid="([^"]+)"'),
        "legend",
    )
    # <layerorder> usa <layer id="..."/>, NO <item>...</item> como <custom-order>
    # (nombres parecidos, formato distinto -- confundirlos fue el primer intento
    # fallido de esta función).
    qgs_text = podar_seccion(
        qgs_text, r"<layerorder\b[^>]*>", "</layerorder>",
        r'<layer id="[^"]*"/>', re.compile(r'id="([^"]+)"'),
        "layerorder",
    )

    # Sobrevive una <relation> solo si AMBOS extremos (referencingLayer y
    # referencedLayer) están en layer_ids -- si layer_ids ya incluye el cierre
    # de dependencias (ver calcular_cierre_dependencias), esto es exactamente
    # lo que hace falta para que el widget RelationReference de, ej., manzana
    # encuentre su relación con intervencion en vez de tirar "Falta
    # dependencia de formulario de capa" (así se detectó este caso).
    m = re.search(r"<relations\b[^>]*>", qgs_text)
    if m:
        cierre_idx = qgs_text.index("</relations>", m.end())
        contenido = qgs_text[m.end():cierre_idx]

        def filtro_relacion(rm):
            bloque = rm.group(0)
            ref_por = re.search(r'referencingLayer="([^"]+)"', bloque)
            ref_do = re.search(r'referencedLayer="([^"]+)"', bloque)
            if ref_por and ref_do and ref_por.group(1) in layer_ids and ref_do.group(1) in layer_ids:
                return bloque
            return ""

        contenido = re.sub(r"<relation\b.*?</relation>", filtro_relacion, contenido, flags=re.S)
        qgs_text = qgs_text[:m.end()] + contenido + qgs_text[cierre_idx:]

    # Los composers de impresión (grandes, ~7k líneas) son irrelevantes para este
    # test y podrían referenciar capas eliminadas -- se vacían enteros. OJO: NO es
    # el <Layouts> chico de <properties>/<Identify> (solo config de UI, "último
    # directorio exportado"), ese se deja como está.
    layouts_pat = re.compile(r"<Layouts>.*?</Layouts>", re.S)
    layouts_matches = list(layouts_pat.finditer(qgs_text))
    grande = max(layouts_matches, key=lambda m: len(m.group(0)), default=None)
    if grande is not None and len(grande.group(0)) > 1000:
        qgs_text = qgs_text[:grande.start()] + "<Layouts>\n  </Layouts>" + qgs_text[grande.end():]

    return qgs_text


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, default=QGIS_GDU_DIR / "gdu.qgz",
                     help="Proyecto .qgz de entrada (default: qgis-gdu/gdu.qgz)")
    ap.add_argument("--output", type=Path, default=QGIS_GDU_DIR / "gdu.wfs.qgz",
                     help="Proyecto .qgz de salida (default: qgis-gdu/gdu.wfs.qgz)")
    ap.add_argument("--geoserver-url", required=True,
                     help="Base URL de GeoServer, ej. http://192.168.0.51:8080/geoserver (SIN /wfs al final)")
    ap.add_argument("--workspace", default="gdu")
    ap.add_argument("--layers", nargs="+", default=["localidad"],
                     help="Una o más capas (nombre en forms/layer_config.py y en GeoServer, "
                          "separadas por espacios). Default: localidad")
    ap.add_argument("--srs", default="EPSG:22175")
    ap.add_argument("--wfs-version", default="auto", help="'auto', '1.1.0' o '2.0.0' (default: auto)")
    ap.add_argument("--username", default=None,
                     help="Opcional: si se omite, QGIS pide credenciales al abrir el proyecto (recomendado para no dejar contraseñas en el .qgz)")
    ap.add_argument("--password", default=None)
    ap.add_argument("--forms-dir", type=Path, default=QGIS_GDU_DIR / "forms")
    ap.add_argument("--force", action="store_true", help="Sobrescribir --output si ya existe")
    ap.add_argument("--solo-esta-capa", action="store_true",
                     help="Además de reconectar, eliminar las capas del proyecto que ni están en "
                          "--layers ni son necesarias por un widget de relación de esas capas "
                          "(ver --pg-host y compañía). Pensado solo para probar sin que QGIS se "
                          "cuelgue pidiendo credenciales de las ~180 capas Postgres restantes -- "
                          "no afecta gdu.qgz ni env/.snipets/gdu/.")
    ap.add_argument("--pg-host", default="192.168.0.51",
                     help="Con --solo-esta-capa: host del Postgres del piloto, para las capas que "
                          "NO están en --layers pero hace falta conservar porque un widget de "
                          "relación de alguna capa de --layers las necesita (ej. manzana/calle/"
                          "vivienda_punto dependen de 'intervención' o 'resolución de costos' para "
                          "el combo de selección) -- esas capas quedan en Postgres normal (de solo "
                          "lectura en la práctica), no se pasan a WFS. Default: el mismo host que "
                          "geoserver/README.md usa para el piloto")
    ap.add_argument("--pg-port", default="5432")
    ap.add_argument("--pg-dbname", default="polizadordbdev")
    ap.add_argument("--pg-schema", default="catastro")
    args = ap.parse_args()

    if args.output.exists() and not args.force:
        sys.exit(f"{args.output} ya existe (usar --force para sobrescribir)")
    if not args.input.exists():
        sys.exit(f"No existe {args.input}")

    config = cargar_layer_config(args.forms_dir)
    layer_ids = {}
    for layer in args.layers:
        if layer not in config:
            sys.exit(f"'{layer}' no está en layer_config.py -- entidades disponibles: {sorted(config)}")
        layer_ids[layer] = config[layer]["id"]

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        with zipfile.ZipFile(args.input) as zin:
            zin.extractall(tmp)

        qgs_candidates = list(tmp.glob("*.qgs"))
        if len(qgs_candidates) != 1:
            sys.exit(f"Se esperaba un único .qgs dentro de {args.input}, se encontraron {len(qgs_candidates)}")
        qgs_path = qgs_candidates[0]

        qgs_text = qgs_path.read_text(encoding="utf-8")
        for layer, layer_id in layer_ids.items():
            datasource_wfs = construir_datasource_wfs(
                args.geoserver_url, args.workspace, layer, args.srs,
                args.wfs_version, args.username, args.password,
            )
            verificar_estructura(qgs_text, layer_id)
            qgs_text, encontrado_maplayer, encontrado_layer_tree = reconectar_texto(qgs_text, layer_id, datasource_wfs)
            if not encontrado_maplayer:
                sys.exit(f"No se pudo reescribir <datasource>/<provider> del maplayer {layer_id} ({layer}) en {qgs_path.name} -- abortando, no se escribió {args.output}")
            if not encontrado_layer_tree:
                print(f"ADVERTENCIA: se reconectó el <maplayer> de '{layer}' pero no se encontró <layer-tree-layer id={layer_id}> "
                      f"(la capa puede no aparecer bien en el panel de capas -- revisar a mano en QGIS)", file=sys.stderr)
            print(f"OK: capa '{layer}' (id={layer_id}) reconectada a WFS -- {datasource_wfs}")

        cierre = set(layer_ids.values())
        if args.solo_esta_capa:
            cierre = calcular_cierre_dependencias(qgs_text, set(layer_ids.values()))
            capas_soporte = cierre - set(layer_ids.values())
            if capas_soporte:
                id_a_nombre = {v["id"]: k for k, v in config.items()}
                for lid in capas_soporte:
                    nombre = id_a_nombre.get(lid, lid)
                    qgs_text, ok_ml, ok_lt = reconectar_postgres_texto(
                        qgs_text, lid, args.pg_host, args.pg_port, args.pg_dbname, args.pg_schema,
                    )
                    if not ok_ml:
                        sys.exit(f"No se pudo reescribir <datasource> de la capa de soporte '{nombre}' ({lid}) -- abortando")
                    if not ok_lt:
                        print(f"ADVERTENCIA: se reconectó el <maplayer> de soporte '{nombre}' pero no su <layer-tree-layer>", file=sys.stderr)
                    print(f"OK: capa de soporte '{nombre}' (id={lid}) reconectada a Postgres del piloto "
                          f"({args.pg_host}:{args.pg_port}/{args.pg_dbname}, schema {args.pg_schema}) -- "
                          f"la necesita un widget de relación de alguna capa de --layers")
            # Solo las capas pedidas que efectivamente tienen geometría deben
            # exigirse en <custom-order>/<legend>/<layerorder> -- ver
            # ids_con_geometria. layer-tree-group/projectlayers (dentro de
            # dejar_solo_estas_capas) siguen exigiendo el cierre completo.
            requeridas_geom = set(layer_ids.values()) & ids_con_geometria(qgs_text)
            qgs_text = dejar_solo_estas_capas(qgs_text, cierre, requeridas_en_todas_lados=requeridas_geom)

        qgs_path.write_text(qgs_text, encoding="utf-8")
        ET.fromstring(qgs_text)  # última validación: el resultado sigue siendo XML bien formado

        args.output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(args.output, "w", zipfile.ZIP_DEFLATED) as zout:
            for f in tmp.iterdir():
                zout.write(f, f.name)

    if args.solo_esta_capa:
        print(f"Recortado: quedan {len(cierre)} capa(s) en el proyecto -- {len(layer_ids)} en WFS-T "
              f"+ {len(cierre) - len(layer_ids)} de soporte en Postgres (el resto se eliminó para esta copia de prueba)")
    print(f"Escrito: {args.output}")
    if not args.username:
        print("Sin --username/--password: QGIS va a pedir credenciales la primera vez que abra cada capa.")


if __name__ == "__main__":
    main()
