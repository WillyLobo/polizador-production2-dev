"""
Motor de renderizado del texto de las resoluciones de certificados de obra.

El texto base de una resolucion no vive en el codigo (a diferencia de viaticos,
ver `secretariador/docx_texto.py`): vive en la base como plantillas Jinja en
`carga.models.TextoResolucionCertificado`, cargadas desde la web por el area.
Este modulo es el que las evalua contra los datos de un Certificado concreto.

Tres piezas:

- `contexto_certificado(certificado)` arma el diccionario de valores. Se apoya
  en `carga.certificado_contexto`, pero proyecta los objetos del ORM a
  namespaces explicitos (`obra.nombre`, `empresa.cuit`, `firmantes.gerente`).
  No es una barrera de seguridad -- Jinja no auto-invoca atributos como si lo
  hace el motor de Django, y `SandboxedEnvironment` ya bloquea lo prefijado con
  "_" -- sino lo que hace posible tener un catalogo de variables enumerable
  (`VARIABLES`) para la paleta del editor y la pagina de ayuda. Las estructuras
  que ya son dicts planos (`resumen`, `desglose_items`, `tramos_ley27397`) se
  pasan tal cual: aplanarlas seria deuda de mantenimiento pura.

- `ENTORNO`, el entorno Jinja restringido, con los filtros de formato que
  necesita un texto legal en castellano (`moneda`, `letras`, `fecha`, ...).
  Todos los filtros son defensivos: un valor `None` o un `Decimal` inesperado
  nunca puede tirar un 500 en la ficha de un certificado.

- `render_bloque` / `render_bloques`, que ademas de devolver el texto reportan
  que variables quedaron sin resolver. Eso importa: una resolucion se firma, y
  emitir un `.docx` con un `«falta: ...»` adentro es peor que no emitirlo.
"""
from decimal import Decimal, InvalidOperation

from jinja2 import ChainableUndefined, TemplateSyntaxError
from jinja2.exceptions import UndefinedError
from jinja2.sandbox import SandboxedEnvironment

from carga.certificado_contexto import _certificado_detalle_context
from carga.templatetags.numletras import numero_a_moneda


class TextoResolucionError(Exception):
    """Error de dominio al compilar o renderizar un bloque de texto.

    Envuelve las excepciones de Jinja para que las vistas puedan mostrarlas como
    un error de formulario en vez de dejarlas propagar como un 500."""


# --------------------------------------------------------------------------- #
# Variables sin resolver
# --------------------------------------------------------------------------- #

def _fabricar_undefined(faltantes):
    """Crea la clase Undefined para un render concreto, que anota en `faltantes`
    cada nombre que la plantilla pidio y el contexto no tenia.

    Es encadenable (`ChainableUndefined`) para que `{{ obra.a.b }}` no explote a
    mitad de cadena: se registra el primer tramo que falto y el resto sigue
    devolviendo undefined hasta que se lo imprime."""

    class _UndefinedQueRegistra(ChainableUndefined):
        __slots__ = ()

        def _nombre(self):
            return self._undefined_name or "?"

        def __str__(self):
            nombre = self._nombre()
            faltantes.add(nombre)
            return f"«falta: {nombre}»"

        # Jinja llama a __html__ cuando hay autoescape; aca no lo hay, pero
        # dejarlo alineado evita que una ruta distinta se saltee el registro.
        def __html__(self):
            return self.__str__()

    return _UndefinedQueRegistra


# --------------------------------------------------------------------------- #
# Filtros
# --------------------------------------------------------------------------- #

def _a_decimal(valor):
    """Decimal o None. Nunca lanza: los filtros se aplican a datos que pueden
    venir nulos (montos UVI de una obra financiada en pesos, por ejemplo)."""
    if valor is None or valor == "":
        return None
    if isinstance(valor, Decimal):
        return valor
    try:
        return Decimal(str(valor))
    except (InvalidOperation, ValueError, TypeError):
        return None


def filtro_moneda(valor, decimales=2):
    """1234567.8 -> '1.234.567,80' (separadores es-AR, sin simbolo)."""
    numero = _a_decimal(valor)
    if numero is None:
        return ""
    entero = f"{numero:,.{decimales}f}"
    return entero.replace(",", "@").replace(".", ",").replace("@", ".")


def filtro_pesos(valor, decimales=2):
    """1234567.8 -> '$1.234.567,80'."""
    texto = filtro_moneda(valor, decimales)
    return f"${texto}" if texto else ""


def filtro_letras(valor):
    """1234.5 -> 'Pesos mil doscientos treinta y cuatro con cincuenta centavos'.

    Envuelve `numletras.numero_a_moneda`, que espera un float y no tolera None."""
    numero = _a_decimal(valor)
    if numero is None:
        return ""
    try:
        return numero_a_moneda(float(numero))
    except (ValueError, TypeError, IndexError, OverflowError):
        return ""


def filtro_fecha(valor, formato="%d/%m/%Y"):
    if valor is None or valor == "":
        return ""
    try:
        return valor.strftime(formato)
    except (AttributeError, ValueError):
        return str(valor)


def filtro_pct(valor, decimales=2):
    """12.3456 -> '12,35 %'."""
    texto = filtro_moneda(valor, decimales)
    return f"{texto} %" if texto else ""


def filtro_mayus(valor):
    return str(valor).upper() if valor is not None else ""


def filtro_cuit(valor):
    """'20123456789' -> '20-12345678-9'. Devuelve el valor tal cual si no tiene
    los 11 digitos (a diferencia del filtro homonimo de numletras, que inventa
    un '00-00000000-0' -- inaceptable en un texto que se firma)."""
    if valor is None:
        return ""
    digitos = "".join(c for c in str(valor) if c.isdigit())
    if len(digitos) != 11:
        return str(valor)
    return f"{digitos[:2]}-{digitos[2:10]}-{digitos[10]}"


FILTROS = {
    "moneda": filtro_moneda,
    "pesos": filtro_pesos,
    "letras": filtro_letras,
    "fecha": filtro_fecha,
    "pct": filtro_pct,
    "mayus": filtro_mayus,
    "cuit": filtro_cuit,
}

# autoescape=False a proposito: la salida es texto plano que va a python-docx,
# no HTML. La vista previa web escapa por su lado, renderizando el resultado a
# traves de `{{ }}` de una plantilla Django.
ENTORNO = SandboxedEnvironment(autoescape=False, keep_trailing_newline=False)
ENTORNO.filters.update(FILTROS)


# --------------------------------------------------------------------------- #
# Contexto
# --------------------------------------------------------------------------- #

def _sin_vacios(datos):
    """Saca las claves sin valor (None o cadena vacia) de una proyeccion.

    Sin esto, un campo nulo (un certificado sin periodo cargado, una obra sin
    convenio) se renderiza como cadena vacia y la resolucion sale diciendo "del
    periodo ," sin que nadie se entere. Al no estar la clave, Jinja la reporta
    como faltante, el editor la muestra y el .docx se frena hasta que se
    complete el dato o se saque la variable del texto.

    Se aplica solo a las proyecciones que arma este modulo, no a las estructuras
    que se pasan tal cual (`resumen`, `desglose_items`, `tramos_ley27397`), donde
    un None es un valor calculado y no un dato sin cargar."""
    if datos is None:
        return None
    limpio = {}
    for clave, valor in datos.items():
        if isinstance(valor, dict):
            valor = _sin_vacios(valor)
        if valor is None or valor == "":
            continue
        limpio[clave] = valor
    return limpio


def _agente(agente):
    """Proyeccion de un personalizador.Agente, o None."""
    if agente is None:
        return None
    return _sin_vacios({
        "nombre": agente.agente_nombres,
        "apellido": agente.agente_apellidos,
        "nombre_completo": agente.agente_nombreyapellido,
        "apellido_nombre": agente.agente_apellidoynombre_coma,
        "abreviatura": agente.abreviatura,
        "cuil": agente.cuil,
        "dni": agente.dni,
    })


def _empresa(empresa):
    if empresa is None:
        return None
    return _sin_vacios({
        "nombre": empresa.empresa_nombre,
        "cuit": empresa.empresa_cuit,
        "titular": empresa.empresa_titular_nombre,
        "titular_titulo": empresa.empresa_titular_titulo,
        "titular_dni": empresa.empresa_titular_dni,
        "direccion": empresa.empresa_direccion,
        "inscripcion": empresa.empresa_inscripcion,
    })


def _obra(obra):
    return _sin_vacios({
        "nombre": obra.obra_nombre,
        "soluciones": obra.obra_soluciones,
        "programa": str(obra.obra_programa) if obra.obra_programa_id else None,
        "empresa": _empresa(obra.obra_empresa),
        "expediente": obra.obra_expediente,
        "expediente_costo": obra.obra_expediente_costo,
        "convenio": obra.obra_convenio,
        "plazo": obra.obra_plazo,
        "grupo": obra.obra_grupo,
        "resolucion": obra.obra_resolucion_display,
        "compulsa": obra.compulsa(),
        "fecha_contrato": obra.obra_fecha_contrato,
        "fecha_entrega": obra.obra_fecha_entrega,
        "localidades": obra.lista_localidades(),
        "nomenclatura": obra.obra_nomenclatura,
        "monto_total_pesos": obra.obra_contrato_total_pesos,
        "monto_total_uvi": obra.obra_contrato_total_uvi,
        "monto_nacion_pesos": obra.obra_contrato_nacion_pesos,
        "monto_provincia_pesos": obra.obra_contrato_provincia_pesos,
        "monto_terceros_pesos": obra.obra_contrato_terceros_pesos,
        "monto_nacion_uvi": obra.obra_contrato_nacion_uvi,
        "monto_provincia_uvi": obra.obra_contrato_provincia_uvi,
        "monto_terceros_uvi": obra.obra_contrato_terceros_uvi,
    })


def _certificado(certificado):
    return _sin_vacios({
        "tipo": certificado.get_certificado_tipo_display(),
        "tipo_codigo": certificado.certificado_tipo,
        "financiamiento": certificado.get_certificado_financiamiento_display(),
        "financiamiento_codigo": certificado.certificado_financiamiento,
        "rubro": str(certificado.certificado_rubro_db) if certificado.certificado_rubro_db_id else None,
        "expediente": certificado.certificado_expediente,
        "periodo": certificado.certificado_periodo,
        "fecha": certificado.certificado_fecha,
        "numero_obra": certificado.certificado_rubro_obra,
        "numero_anticipo": certificado.certificado_rubro_anticipo,
        "numero_devanticipo": certificado.certificado_rubro_devanticipo,
        "monto_pesos": certificado.certificado_monto_pesos,
        "monto_uvi": certificado.certificado_monto_uvi,
        "monto_cobrar_pesos": certificado.certificado_monto_cobrar,
        "monto_cobrar_uvi": certificado.certificado_monto_cobrar_uvi,
        "devolucion_pesos": certificado.certificado_devolucion_monto,
        "devolucion_uvi": certificado.certificado_devolucion_monto_uvi,
        "devolucion_expediente": certificado.certificado_devolucion_expte,
        "descuento_anticipo_pesos": certificado.certificado_descuento_anticipo_pesos,
        "descuento_anticipo_uvi": certificado.certificado_descuento_anticipo_uvi,
        "descuento_anticipo_pct": certificado.certificado_descuento_anticipo_pct,
        "fondoreparo_pct": certificado.certificado_fondoreparo_pct,
        "fondoreparo_pesos": certificado.certificado_fondoreparo_monto_pesos(),
        "fondoreparo_uvi": certificado.certificado_fondoreparo_monto_uvi(),
        "mes_pct": certificado.certificado_mes_pct,
        "anterior_pct": certificado.certificado_ante_pct,
        "acumulado_pct": certificado.certificado_acum_pct,
        "pct_principal": certificado.certificado_pct_principal,
        "anticipo_pct": certificado.certificado_anticipo_pct,
        "anticipo_acumulado_pct": certificado.certificado_anticipo_acumulado,
        "anticipo_saldo_pct": certificado.certificado_anticipo_saldo_pct,
        "etapa_pct": certificado.certificado_etapa_pct,
    })


def contexto_certificado(certificado, detalle=None):
    """Diccionario de valores contra el que se renderiza el texto de la
    resolucion de `certificado`.

    `detalle` permite inyectar un `_certificado_detalle_context` ya calculado:
    esa funcion dispara `resumen_certificacion_mensual` y varias queries, asi
    que en una vista que ademas muestra la ficha conviene computarlo una sola
    vez por request en lugar de dos."""
    if detalle is None:
        detalle = _certificado_detalle_context(certificado)

    obra = detalle["obra"]
    financiamiento = detalle["financiamiento"]
    contratomonto_rubro = detalle["contratomonto_rubro"]
    plan = detalle["plan"]

    return {
        "obra": _obra(obra),
        "certificado": _certificado(certificado),
        "empresa": _empresa(obra.obra_empresa),
        "financiamiento": _sin_vacios({
            "nombre": financiamiento.certificadofinanciamiento_nombre if financiamiento else None,
            "codigo": financiamiento.certificadofinanciamiento_nombre_corto if financiamiento else None,
        }),
        "contrato": _sin_vacios({
            "monto_pesos": contratomonto_rubro.contratomonto_pesos if contratomonto_rubro else None,
            "monto_uvi": contratomonto_rubro.contratomonto_uvi if contratomonto_rubro else None,
            "incidencia_pct_pesos": detalle["incidencia_pct_pesos"],
            "incidencia_pct_uvi": detalle["incidencia_pct_uvi"],
        }),
        "plan": _sin_vacios({
            "fecha": plan.trabajos_fecha if plan else None,
            "fecha_inicio": plan.trabajos_fecha_inicio if plan else None,
            "meses": plan.trabajos_meses if plan else None,
        }),
        "uvi": _sin_vacios({
            "fecha": detalle["uvi_fecha_calculo"],
            "valor": detalle["uvi_valor_calculo"],
        }),
        "firmantes": _sin_vacios({
            "presidente": _agente(
                detalle["presidente"].directorio_autoridad_a_cargo_fk if detalle["presidente"] else None
            ),
            "gerente": _agente(detalle["hoja1_firmantes"][0]["agente"]),
            "directora": _agente(detalle["hoja2_firmantes"][0]["agente"]),
            "jefe": _agente(detalle["hoja3_firmantes"][0]["agente"]),
        }),
        # Ya son dicts planos: se pasan tal cual.
        "resumen": detalle["resumen"],
        "desglose_items": detalle["desglose_items"],
        "tramos_ley27397": detalle["tramos_ley27397"],
    }


# --------------------------------------------------------------------------- #
# Catalogo de variables (paleta del editor + pagina de ayuda)
# --------------------------------------------------------------------------- #

VARIABLES = [
    ("Obra", [
        ("obra.nombre", "Nombre de la obra tal como figura en el contrato"),
        ("obra.soluciones", "Cantidad de soluciones habitacionales"),
        ("obra.programa", "Programa al que pertenece"),
        ("obra.expediente", "Expediente de la obra"),
        ("obra.convenio", "Convenio / ACU"),
        ("obra.plazo", "Plazo de ejecución"),
        ("obra.resolucion", "Resolución de adjudicación"),
        ("obra.compulsa", "Tipo y número de licitación"),
        ("obra.localidades", "Localidades de la obra"),
        ("obra.fecha_contrato|fecha", "Fecha de firma del contrato"),
        ("obra.monto_total_pesos|pesos", "Monto total de contrato en pesos"),
        ("obra.monto_total_uvi|moneda", "Monto total de contrato en UVI"),
    ]),
    ("Empresa", [
        ("empresa.nombre", "Razón social de la contratista"),
        ("empresa.cuit|cuit", "CUIT de la contratista"),
        ("empresa.titular_titulo", "Título del representante (Sr., Ing., ...)"),
        ("empresa.titular", "Titular de la empresa"),
        ("empresa.direccion", "Domicilio de la empresa"),
    ]),
    ("Certificado", [
        ("certificado.tipo", "Tipo de certificado, en texto"),
        ("certificado.financiamiento", "Financiamiento, en texto (Nación/Provincia/Terceros)"),
        ("certificado.rubro", "Rubro certificado"),
        ("certificado.expediente", "Expediente del certificado"),
        ("certificado.periodo", "Período certificado"),
        ("certificado.fecha|fecha", "Fecha del certificado"),
        ("certificado.numero_obra", "Número correlativo de certificado de obra"),
        ("certificado.numero_anticipo", "Número correlativo de anticipo"),
        ("certificado.monto_pesos|pesos", "Monto bruto en pesos"),
        ("certificado.monto_pesos|letras", "Monto bruto en pesos, escrito en letras"),
        ("certificado.monto_uvi|moneda", "Monto bruto en UVI"),
        ("certificado.monto_cobrar_pesos|pesos", "Monto a cobrar en pesos"),
        ("certificado.fondoreparo_pct|pct", "Porcentaje de fondo de reparo"),
        ("certificado.fondoreparo_pesos|pesos", "Fondo de reparo en pesos"),
        ("certificado.descuento_anticipo_pesos|pesos", "Descuento de anticipo en pesos"),
        ("certificado.mes_pct|pct", "Avance del mes"),
        ("certificado.acumulado_pct|pct", "Avance acumulado"),
        ("certificado.anticipo_pct|pct", "Porcentaje de anticipo otorgado"),
    ]),
    ("Contrato y UVI", [
        ("contrato.monto_pesos|pesos", "Monto de contrato del rubro y financiamiento, en pesos"),
        ("contrato.monto_uvi|moneda", "Monto de contrato del rubro y financiamiento, en UVI"),
        ("uvi.valor|moneda", "Cotización UVI usada para el cálculo"),
        ("uvi.fecha|fecha", "Fecha de esa cotización"),
    ]),
    ("Resumen de certificación", [
        ("resumen.unidad", "Unidad del resumen ('UVI' o '$')"),
        ("resumen.total_general.total_pesos|pesos", "Total general acumulado en pesos"),
        ("resumen.subtotal1.mes_pesos|pesos", "Subtotal 1 del mes, en pesos"),
        ("resumen.fondo_reparo.mes_pesos|pesos", "Fondo de reparo del mes, en pesos"),
        ("resumen.anticipo.total_pct|pct", "Anticipo acumulado, en porcentaje"),
    ]),
    ("Firmantes", [
        ("firmantes.presidente.nombre_completo", "Presidente del IPDUV"),
        ("firmantes.gerente.nombre_completo", "Gerente Operativo"),
        ("firmantes.directora.nombre_completo", "Directora de Certificaciones"),
        ("firmantes.jefe.nombre_completo", "Jefe del Depto. de Certificados de Obras"),
    ]),
]

FILTROS_DOC = [
    ("|pesos", "Formato moneda con símbolo: $1.234.567,80"),
    ("|moneda", "Formato moneda sin símbolo: 1.234.567,80"),
    ("|letras", "Importe escrito en letras"),
    ("|fecha", "Fecha en dd/mm/aaaa"),
    ("|pct", "Porcentaje: 12,35 %"),
    ("|mayus", "Todo en mayúsculas"),
    ("|cuit", "CUIT con guiones: 20-12345678-9"),
]


# --------------------------------------------------------------------------- #
# Render
# --------------------------------------------------------------------------- #

def compilar_bloque(texto):
    """Compila sin renderizar. Lo usan los forms para validar al guardar: sin
    esto, un `{%` suelto en una plantilla rompe la ficha de todos los
    certificados que caen en su alcance."""
    try:
        return ENTORNO.from_string(texto or "")
    except TemplateSyntaxError as e:
        raise TextoResolucionError(f"Error de sintaxis en la línea {e.lineno}: {e.message}") from e


def render_bloque(texto, contexto):
    """Devuelve `(texto_renderizado, faltantes)`.

    `faltantes` es el conjunto de variables que la plantilla pidio y el contexto
    no tenia; en el texto aparecen como `«falta: nombre»`."""
    faltantes = set()
    entorno = ENTORNO.overlay(undefined=_fabricar_undefined(faltantes))
    try:
        plantilla = entorno.from_string(texto or "")
        return plantilla.render(**contexto), faltantes
    except TemplateSyntaxError as e:
        raise TextoResolucionError(f"Error de sintaxis en la línea {e.lineno}: {e.message}") from e
    except UndefinedError as e:
        raise TextoResolucionError(f"Variable inválida: {e.message}") from e
    except Exception as e:  # noqa: BLE001 - cualquier error de una plantilla cargada por el usuario
        raise TextoResolucionError(f"Error al renderizar: {e}") from e


def render_bloques(bloques, contexto):
    """Renderiza la lista de bloques de un TextoResolucionCertificado.

    Devuelve `(bloques_renderizados, faltantes)`, donde cada bloque conserva su
    `clase` y `label` y reemplaza `texto` por el texto ya resuelto."""
    faltantes = set()
    resueltos = []
    for bloque in bloques or []:
        texto, faltan = render_bloque(bloque.get("texto", ""), contexto)
        faltantes |= faltan
        resueltos.append({
            "clase": bloque.get("clase", "considerando"),
            "label": bloque.get("label", ""),
            "texto": texto,
        })
    return resueltos, faltantes
