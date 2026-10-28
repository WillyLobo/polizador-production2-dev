"""
Arma el proyecto QGIS de GDU (gdu-oapif.qgz) contra las colecciones OGC API - Features
de polizador (gdu/oapif.py). Reemplaza al gdu.qgz heredado, que apuntaba a Postgres o a
GeoServer y necesitaba forms/*.ui + nn.py al lado.

Todo sale de los schemas del servidor: los campos, los alias (verbose_name), los combos de
las choices (x-gdu-etiquetas) y las relaciones (x-ogc-collectionId de cada FK). Acá solo
se decide lo que el servidor no sabe: grupos del panel de capas, cómo se muestra cada
registro en los combos, qué listas hijas lleva cada formulario y a qué escala se dibuja.
Una colección nueva en el servidor aparece sola, en el grupo "Otras".

Los formularios son los nativos de QGIS (arrastrar y soltar): no hay código Python en el
proyecto, así que el .qgz se reparte solo, sin carpeta forms/.

Uso (en la máquina con QGIS, sin abrir QGIS):

    "C:\\Program Files\\QGIS 3.44.14\\bin\\python-qgis-ltr.bat" armar_proyecto.py ^
        --url http://192.168.0.51:8000/gdu/oapif/ --usuario oapif_lector --salida gdu-oapif.qgz

La clave se pide por consola (o GDU_OAPIF_CLAVE). Hace falta un usuario que vea todas las
colecciones (grupo "GDU: Lectores QGIS"). El proyecto guarda solo el id de autenticación
(--authcfg, por defecto gduoapf): cada usuario crea una vez en su QGIS una configuración
Basic con ese mismo id (ver README.md).
"""
import argparse
import base64
import getpass
import json
import os
import sys
import tempfile
import urllib.request

AUTHCFG = "gduoapf"
# patrón para la capa completa de parcelas y las de cada zona (no parcelas_expropiadas)
PARCELAS = "<parcelas>"
CRS_PROYECTO = "EPSG:22175"
# features por pedido. Cada página le cuesta al servidor un COUNT y un OFFSET sobre la tabla
# entera, más allá de su tamaño: bajar catastro_urbano completo (430.000 filas, lo que hace
# la tabla de atributos) tardaba 131 s de servidor en páginas de 1000 y 31 s en páginas de 10.000.
TAMANO_PAGINA = 10000

# grupo del panel de capas -> colecciones, de arriba hacia abajo. "*" toma las colecciones
# cuyo id empieza así, en el orden del servidor; PARCELAS, las capas de parcelas.
GRUPOS = [
    ("Capas", [
        "viviendas_punto", "pre_adjudicatarios_dispersa", "calles", "ufs", "manzanas", "barrios",
        "parcelas_expropiadas", "tierras", "planos_mensura",
    ]),
    ("Parcelas", ["parcelas_dpto_*", "parcelas_resistencia_*", "parcelas", "zonas_parcelas"]),
    ("Viviendas (consultas)", [
        "viviendas_sin_plan_grupo", "viviendas_con_plan_grupo_sin_adjudicatario", "viviendas_para_escriturar",
    ]),
    ("Referencia", ["catastro_urbano"]),
    ("Tablas", [
        "programas", "actuaciones", "contrataciones", "intervenciones", "ejecutores", "inspectores",
        "expropiaciones", "adjudicaciones_beneficiario", "resoluciones_costos", "tierras_consultas",
        "intervenciones_ejecutores", "intervenciones_inspectores", "planos_mensura_intervencion",
        "planos_mensura_tierra", "localidades", "adjudicatarios_3450",
    ]),
    ("Tablas de tipos", [
        "tipos_contratacion", "tipos_intervencion", "tipos_ejecutor", "destinos_parcela", "tierra_destinos",
        "tipos_doc_probatoria", "estados_gestion_expropiacion", "objetos_expropiacion",
    ]),
]
# visibles al abrir el proyecto; el resto queda apagado para no descargar todo de entrada
VISIBLES = {"barrios", "manzanas", "calles", "planos_mensura", "viviendas_punto"}
# escala mínima (1:N) a partir de la cual se dibujan las capas grandes
ESCALAS = {
    "catastro_urbano": 10000, PARCELAS: 25000, "ufs": 25000, "viviendas_sin_plan_grupo": 25000,
    "viviendas_con_plan_grupo_sin_adjudicatario": 25000, "viviendas_para_escriturar": 25000,
}

# cómo se muestra un registro en los combos de las FK (por defecto "nombre", si existe)
MOSTRAR = {
    "actuaciones": "\"nombre\" || ' (' || \"ano\" || ')'",
    "contrataciones": "coalesce(nullif(\"nombre\", ''), nullif(\"expediente\", ''), \"resolucion\")",
    "adjudicaciones_beneficiario": "\"nro\" || '/' || \"ano\" || ' (' || \"tipo\" || ')'",
    "resoluciones_costos": "\"nro_largo\" || '/' || \"nro_corto\" || ' - ' || \"ano\" || ' (' || \"tipo\" || ')'",
    "planos_mensura": "\"depto\" || '-' || \"nro\" || '-' || \"ano\"",
    PARCELAS: "coalesce(\"nomenclatura\", 'Parcela ' || \"id\")",
    # parcela_nomenclatura la agrega el servidor (la FK parcela es un id interno)
    "ufs": "'UF ' || \"uf\" || coalesce(' - ' || \"parcela_nomenclatura\", ' (parcela ' || \"parcela\" || ')')",
    "tierras": "coalesce(nullif(\"propietario\", ''), \"nomenclatura\", 'Tierra ' || \"id\")",
    "expropiaciones": "'Ley ' || \"nro_ley\" || coalesce(\"letra_ley\", '') || coalesce('/' || \"ano_ley\", '')",
    "parcelas_expropiadas": "coalesce(\"nomenclatura\", 'Parcela expropiada ' || \"id\")",
    "localidades": "\"localidad_nombre\"",
    **{coleccion_id: "'UF ' || \"uf\" || coalesce(' - ' || \"parcela_nomenclatura\", '')" for coleccion_id in (
        "viviendas_sin_plan_grupo", "viviendas_con_plan_grupo_sin_adjudicatario", "viviendas_para_escriturar",
    )},
    "adjudicatarios_3450": "\"nro_adjudicatario\" || ' - ' || \"apellido_nombre\"",
}
# FK que quedan como número: el combo carga la tabla referenciada entera (~70.000 adjudicatarios,
# ~65.000 parcelas; 25-30 s al abrir la tabla de atributos). Las consultas de viviendas son de
# solo lectura, no necesitan el combo.
VIVIENDAS_CONSULTA = ("viviendas_sin_plan_grupo", "viviendas_con_plan_grupo_sin_adjudicatario", "viviendas_para_escriturar")
FK_SIN_COMBO = {("ufs", "adjudicatario"), ("viviendas_punto", "adjudicatario")} | {
    (coleccion_id, campo) for coleccion_id in VIVIENDAS_CONSULTA for campo in ("adjudicatario", "parcela")
}

# listas hijas en el formulario del padre: (padre, tabla hija, FK al padre, FK al otro lado si es N:M).
# Las N:M con datos propios en la tabla intermedia (el tipo de vínculo de los planos) van 1:N,
# así QGIS pide el tipo al vincular.
LISTAS = [
    ("programas", "Actuaciones", "actuaciones", "programa", None),
    ("actuaciones", "Contrataciones", "contrataciones", "actuacion", None),
    ("contrataciones", "Intervenciones", "intervenciones", "contratacion", None),
    ("intervenciones", "Ejecutores", "intervenciones_ejecutores", "intervencion", "ejecutor"),
    ("intervenciones", "Inspectores", "intervenciones_inspectores", "intervencion", "inspector"),
    ("intervenciones", "Planos de mensura", "planos_mensura_intervencion", "intervencion", None),
    ("planos_mensura", "Intervenciones", "planos_mensura_intervencion", "plano", None),
    ("planos_mensura", "Tierras", "planos_mensura_tierra", "plano", None),
    ("tierras", "Planos de mensura", "planos_mensura_tierra", "tierra", None),
    ("tierras", "Consultas", "tierras_consultas", "tierra", None),
    ("expropiaciones", "Parcelas expropiadas", "parcelas_expropiadas", "expropiacion", None),
    (PARCELAS, "Unidades funcionales", "ufs", "parcela", None),
]
AUDITORIA = {"id": "ID", "updated_at": "Modificado", "updated_by": "Modificado por (usuario)"}

COLORES = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#a65628", "#f781bf", "#999999", "#17becf"]
OSM = "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0"


def coincide(patron, coleccion_id):
    if patron == PARCELAS:
        return coleccion_id == "parcelas" or coleccion_id.startswith(("parcelas_dpto_", "parcelas_resistencia_"))
    return coleccion_id.startswith(patron[:-1]) if patron.endswith("*") else coleccion_id == patron


def valor_por_patron(tabla, coleccion_id, defecto=None):
    for patron, valor in tabla.items():
        if coincide(patron, coleccion_id):
            return valor
    return defecto


class Servidor:
    def __init__(self, url, usuario, clave):
        self.url = url if url.endswith("/") else url + "/"
        self.auth = "Basic " + base64.b64encode(f"{usuario}:{clave}".encode()).decode()

    def get(self, ruta, accept="application/json"):
        pedido = urllib.request.Request(self.url + ruta, headers={"Authorization": self.auth, "Accept": accept})
        with urllib.request.urlopen(pedido) as respuesta:
            return json.load(respuesta)

    def colecciones(self):
        return [c["id"] for c in self.get("collections")["collections"]]

    def schema(self, coleccion_id):
        return self.get(f"collections/{coleccion_id}/schema", "application/schema+json")


def ordenar_en_grupos(ids):
    """[(grupo, [ids])] con cada colección del servidor una sola vez; lo no previsto va a "Otras"."""
    usados, grupos = set(), []
    for nombre, patrones in GRUPOS:
        elegidos = []
        for patron in patrones:
            for coleccion_id in ids:
                if coincide(patron, coleccion_id) and coleccion_id not in usados:
                    elegidos.append(coleccion_id)
                    usados.add(coleccion_id)
        grupos.append((nombre, elegidos))
    grupos.append(("Otras", [c for c in ids if c not in usados]))
    return [(nombre, elegidos) for nombre, elegidos in grupos if elegidos]


def armar(args):
    from qgis.core import (
        Qgis, QgsApplication, QgsAttributeEditorContainer, QgsAttributeEditorField, QgsAttributeEditorRelation,
        QgsAuthMethodConfig, QgsCoordinateReferenceSystem, QgsEditorWidgetSetup, QgsProject, QgsRasterLayer,
        QgsRelation, QgsSymbol, QgsVectorLayer,
    )
    from qgis.PyQt.QtGui import QColor

    servidor = Servidor(args.url, args.usuario, args.clave)
    ids = servidor.colecciones()
    schemas = {coleccion_id: servidor.schema(coleccion_id) for coleccion_id in ids}
    print(f"{len(ids)} colecciones en {servidor.url}")

    # base de autenticación descartable, con el mismo id que van a tener los usuarios
    os.environ["QGIS_AUTH_DB_DIR_PATH"] = tempfile.mkdtemp(prefix="gdu-auth-")
    app = QgsApplication([], False)
    app.initQgis()
    auth = QgsApplication.authManager()
    auth.setMasterPassword("armar-proyecto", True)
    config = QgsAuthMethodConfig("Basic")
    config.setId(args.authcfg)
    config.setName("GDU OAPIF")
    config.setConfig("username", args.usuario)
    config.setConfig("password", args.clave)
    if not auth.storeAuthenticationConfig(config, True):
        sys.exit("No se pudo guardar la configuración de autenticación")

    proyecto = QgsProject.instance()
    proyecto.setTitle("GDU - IPDUV")
    proyecto.setCrs(QgsCoordinateReferenceSystem(CRS_PROYECTO))

    capas = {}
    for i, coleccion_id in enumerate(ids):
        uri = (
            f"url='{servidor.url}' typename='{coleccion_id}' authcfg='{args.authcfg}' pagingEnabled='true' "
            f"pageSize='{TAMANO_PAGINA}' restrictToRequestBBOX='1' preferCoordinatesForWfsT11='false'"
        )
        titulo = schemas[coleccion_id].get("title", coleccion_id)
        capa = QgsVectorLayer(uri, titulo, "OAPIF")
        if not capa.isValid():
            # una colección que el servidor no puede servir no frena el resto: queda fuera del proyecto
            print(f"AVISO: no carga la colección {coleccion_id}, queda fuera del proyecto", file=sys.stderr)
            continue
        if capa.isSpatial():
            simbolo = QgsSymbol.defaultSymbol(capa.geometryType())
            color = QColor(COLORES[i % len(COLORES)])
            if capa.geometryType() == Qgis.GeometryType.Polygon:
                simbolo.symbolLayer(0).setFillColor(QColor(color.red(), color.green(), color.blue(), 40))
                simbolo.symbolLayer(0).setStrokeColor(color)
            else:
                simbolo.setColor(color)
            capa.renderer().setSymbol(simbolo)
            if escala := valor_por_patron(ESCALAS, coleccion_id):
                capa.setScaleBasedVisibility(True)
                capa.setMinimumScale(escala)
        proyecto.addMapLayer(capa, False)
        capas[coleccion_id] = capa

    # cómo se muestra cada registro en los combos
    for coleccion_id, capa in capas.items():
        nombres = capa.fields().names()
        expresion = valor_por_patron(MOSTRAR, coleccion_id, '"nombre"' if "nombre" in nombres else '"id"')
        capa.setDisplayExpression(expresion)

    # una relación por FK, hacia la colección que dice el servidor
    relaciones = proyecto.relationManager()

    def clave(coleccion_id):
        """campo clave de la colección (x-ogc-role: id); "id" salvo, p. ej., adjudicatarios_3450"""
        propiedades = schemas[coleccion_id]["properties"]
        return next((n for n, p in propiedades.items() if p.get("x-ogc-role") == "id"), "id")

    def relacion(hija_id, campo, padre_id):
        rel = QgsRelation()
        rel.setId(f"{hija_id}__{campo}__{padre_id}")
        rel.setName(f"{capas[hija_id].name()} - {campo}")
        rel.setReferencingLayer(capas[hija_id].id())
        rel.setReferencedLayer(capas[padre_id].id())
        rel.addFieldPair(campo, clave(padre_id))
        if not rel.isValid():
            sys.exit(f"Relación inválida: {rel.id()} ({rel.validationError()})")
        relaciones.addRelation(rel)
        return rel

    def padre_de(propiedad):
        destinos = propiedad.get("x-ogc-collectionId")
        if not destinos:
            return None
        destinos = [destinos] if isinstance(destinos, str) else destinos
        # una FK a parcela apunta a las 30 capas de parcelas: el combo usa la completa
        return "parcelas" if "parcelas" in destinos else destinos[0]

    for coleccion_id, capa in capas.items():
        schema = schemas[coleccion_id]
        requeridos = set(schema.get("required", []))
        campos = capa.fields()
        for nombre, propiedad in schema["properties"].items():
            idx = campos.indexOf(nombre)
            if idx < 0:
                continue  # la geometría
            capa.setFieldAlias(idx, AUDITORIA.get(nombre, propiedad.get("title", nombre)))
            nulo = nombre not in requeridos
            padre_id = padre_de(propiedad)
            if padre_id in capas and (coleccion_id, nombre) not in FK_SIN_COMBO:
                rel = relacion(coleccion_id, nombre, padre_id)
                capa.setEditorWidgetSetup(idx, QgsEditorWidgetSetup("RelationReference", {
                    "Relation": rel.id(), "AllowNULL": nulo, "OrderByValue": True, "ShowForm": False,
                    "ShowOpenFormButton": True, "MapIdentification": capas[padre_id].isSpatial(),
                    "AllowAddFeatures": False, "ReadOnly": False,
                }))
            elif etiquetas := propiedad.get("x-gdu-etiquetas"):
                # el vacío de una choice de texto es "" en el servidor (CharField blank). Con "" el
                # combo muestra "(vacío)" en esos registros; al leer el proyecto QGIS lo vuelve NULL
                # al guardar, y el servidor guarda NULL como "" (ColeccionGdu.save_model)
                vacio = "" if propiedad.get("type") == "string" else "{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}"
                mapa = ([{"(vacío)": vacio}] if nulo else [])
                mapa += [{etiqueta: valor} for valor, etiqueta in etiquetas.items()]
                capa.setEditorWidgetSetup(idx, QgsEditorWidgetSetup("ValueMap", {"map": mapa}))

    # formularios: pestaña de datos, una por lista hija y la auditoría al final
    for coleccion_id, capa in capas.items():
        schema = schemas[coleccion_id]
        solo_lectura = {n for n, p in schema["properties"].items() if p.get("readOnly")} | {"id"}
        form = capa.editFormConfig()
        form.setLayout(Qgis.AttributeFormLayout.DragAndDrop)
        raiz = form.invisibleRootContainer()
        raiz.clear()
        datos = QgsAttributeEditorContainer("Datos", raiz)
        datos.setType(Qgis.AttributeEditorContainerType.Tab)
        auditoria = QgsAttributeEditorContainer("Auditoría", raiz)
        auditoria.setType(Qgis.AttributeEditorContainerType.Tab)
        for idx, campo in enumerate(capa.fields()):
            contenedor = auditoria if campo.name() in AUDITORIA else datos
            contenedor.addChildElement(QgsAttributeEditorField(campo.name(), idx, contenedor))
            if campo.name() in solo_lectura:
                form.setReadOnly(idx, True)
        raiz.addChildElement(datos)
        for padre, titulo, hija_id, campo_padre, campo_otro in LISTAS:
            if not coincide(padre, coleccion_id) or hija_id not in capas:
                continue
            # la de la FK ya existe salvo para las capas de parcelas por zona
            rel = relaciones.relation(f"{hija_id}__{campo_padre}__{coleccion_id}")
            if not rel.isValid():
                rel = relacion(hija_id, campo_padre, coleccion_id)
            pestana = QgsAttributeEditorContainer(titulo, raiz)
            pestana.setType(Qgis.AttributeEditorContainerType.Tab)
            editor = QgsAttributeEditorRelation(rel, pestana)
            editor.setLabel(titulo)
            if campo_otro:
                otro = padre_de(schemas[hija_id]["properties"][campo_otro])
                editor.setNmRelationId(f"{hija_id}__{campo_otro}__{otro}")
            pestana.addChildElement(editor)
            raiz.addChildElement(pestana)
        raiz.addChildElement(auditoria)
        capa.setEditFormConfig(form)

    # panel de capas
    arbol = proyecto.layerTreeRoot()
    for nombre, elegidos in ordenar_en_grupos(list(capas)):
        grupo = arbol.addGroup(nombre)
        grupo.setExpanded(nombre == "Capas")
        for coleccion_id in elegidos:
            nodo = grupo.addLayer(capas[coleccion_id])
            nodo.setItemVisibilityChecked(coleccion_id in VISIBLES)
            nodo.setExpanded(False)
    base = QgsRasterLayer(OSM, "OpenStreetMap", "wms")
    proyecto.addMapLayer(base, False)
    arbol.addGroup("Capas base").addLayer(base)

    if not proyecto.write(args.salida):
        sys.exit(f"No se pudo escribir {args.salida}")
    print(f"Escrito {args.salida}: {len(capas)} capas, {len(relaciones.relations())} relaciones")
    proyecto.clear()
    app.exitQgis()


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--url", required=True, help="raíz OAPIF, p. ej. https://polizador.../gdu/oapif/")
    parser.add_argument("--usuario", required=True, help="usuario con lectura de todas las colecciones")
    parser.add_argument("--clave", default=os.environ.get("GDU_OAPIF_CLAVE"))
    parser.add_argument("--authcfg", default=AUTHCFG, help=f"id de autenticación que guarda el proyecto ({AUTHCFG})")
    parser.add_argument("--salida", default="gdu-oapif.qgz")
    args = parser.parse_args()
    if not args.clave:
        args.clave = getpass.getpass(f"Clave de {args.usuario}: ")
    armar(args)


if __name__ == "__main__":
    main()
