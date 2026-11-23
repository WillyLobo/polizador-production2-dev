"""Instrumentos legales de un Agente: tabla de conceptos y matcher de texto heredado.

Antes cada instrumento del Agente (pase a planta, bonificacion, contrato de servicio, ...)
se cargaba como texto libre "Numero/Año" + un `_tipo` RES/DEC/DIS. Ahora cada instrumento
es una fila de AgenteInstrumento (un agente puede tener varios por concepto) que apunta por
FK a InstrumentosLegalesResoluciones / InstrumentosLegalesDecretos (secretariador) o a
InstrumentoAgente (instrumentos de otros organismos). Los textos que no se pudieron vincular
quedan en las columnas viejas del Agente ("dato heredado") hasta que alguien los vincule;
`buscar` es el matcher que usan el comando vincular_instrumentos_agente, el importador
importar_informe_ipduv y la data migration de aportes.

No importa personalizador.models a nivel modulo (models.py importa este archivo).
"""
import re
from collections import namedtuple

from django.db import models

RES, DEC, EXT = "RES", "DEC", "EXT"

TIPO_LABELS = {RES: "Resolución", DEC: "Decreto", EXT: "Externo"}

CAMPO_POR_TIPO = {RES: "resolucion", DEC: "decreto", EXT: "externo"}
"""Campo FK de AgenteInstrumento que corresponde a cada tipo de instrumento."""

Concepto = namedtuple("Concepto", "clave label heredado heredado_tipo tipo_fijo tipos con_tiempo")
"""
- clave: valor de AgenteInstrumento.concepto.
- heredado / heredado_tipo: columnas de texto viejas del Agente (heredado_tipo None si el
  concepto nunca tuvo `_tipo`: en ese caso se asume `tipo_fijo`).
- tipos: tipos de instrumento (RES/DEC/EXT) admitidos, en el orden en que se ofrecen en el form.
- con_tiempo: cada instrumento reconoce años/meses/dias de antigüedad (aportes).
"""

CONCEPTOS = (
    Concepto("pase_planta", "Pase a planta permanente", "n_decreto", None, DEC, (DEC,), False),
    Concepto("bonificacion", "Bonificación por título", "instrumento_bonificacion", "instrumento_bonificacion_tipo", None, (RES, DEC), False),
    Concepto("contrato_servicio", "Contrato de servicio", "instrumento_contrato_de_servicio", "instrumento_contrato_de_servicio_tipo", None, (RES, DEC), False),
    Concepto("cargo_interno", "Designación temporal", "instrumento_cargo_interno", "instrumento_cargo_interno_tipo", None, (RES, DEC), False),
    Concepto("transferencia_definitiva", "Transferencia definitiva", "n_decreto_transferencia_definitiva", None, DEC, (DEC, EXT), False),
    Concepto("aportes_ley", "Aportes (Ley/Resolución)", "aportes_ley_resolucion", "aportes_ley_resolucion_tipo", None, (RES, DEC, EXT), True),
    Concepto("aportes_anses", "Aportes (ANSES)", "aportes_anses", None, EXT, (EXT,), True),
)

CONCEPTOS_POR_CLAVE = {c.clave: c for c in CONCEPTOS}

CONCEPTO_CHOICES = [(c.clave, c.label) for c in CONCEPTOS]


def url_documento(instrumento):
    """(url, es_pdf): el PDF digitalizado del instrumento si tiene, si no su pagina de edicion."""
    for field in instrumento._meta.fields:
        if isinstance(field, models.FileField) and getattr(instrumento, field.name):
            return getattr(instrumento, field.name).url, True
    return instrumento.get_absolute_url(), False


def tipo_heredado(agente, concepto):
    """Tipo (RES/DEC/DIS) del texto heredado, o None si no se cargo."""
    if concepto.heredado_tipo:
        return getattr(agente, concepto.heredado_tipo) or None
    return concepto.tipo_fijo if concepto.tipo_fijo != EXT else None


def limpiar_heredado(agente, concepto):
    """Vacia el texto heredado (y su tipo) del concepto. Devuelve los campos tocados."""
    setattr(agente, concepto.heredado, None)
    campos = [concepto.heredado]
    if concepto.heredado_tipo:
        setattr(agente, concepto.heredado_tipo, None)
        campos.append(concepto.heredado_tipo)
    return campos


def asignar(agente, concepto, tipo, instrumento):
    """Agrega `instrumento` (de tipo RES/DEC/EXT) a los instrumentos del concepto del agente
    (ya guardado) y devuelve la fila de AgenteInstrumento.

    Si ya estaba, devuelve esa fila. En los conceptos con tiempo (aportes), si hay una fila
    sin instrumento (años reconocidos que todavia no tenian respaldo) se completa esa en vez
    de crear otra, para no separar el tiempo del instrumento que lo reconoce."""
    campo = CAMPO_POR_TIPO[tipo]
    filas = agente.instrumentos_legales.filter(concepto=concepto.clave)
    existente = filas.filter(**{campo: instrumento}).first()
    if existente:
        return existente
    if concepto.con_tiempo:
        sin_instrumento = filas.filter(resolucion__isnull=True, decreto__isnull=True, externo__isnull=True).first()
        if sin_instrumento:
            setattr(sin_instrumento, campo, instrumento)
            sin_instrumento.save()
            return sin_instrumento
    return agente.instrumentos_legales.create(concepto=concepto.clave, **{campo: instrumento})


# --- Matcher -------------------------------------------------------------------------

def _anio(texto):
    if len(texto) == 4:
        return texto
    if len(texto) == 2:
        return f"20{texto}" if int(texto) < 50 else f"19{texto}"
    return None


def parsear(texto):
    """'940/32/2015' -> (940, '32', '2015'); '0038-21' -> (38, None, '2021').

    Separadores aceptados: '/', '-' y espacios. Devuelve None si el texto no es
    numero[/acta]/año con todas sus partes numericas."""
    if not texto:
        return None
    partes = [p for p in re.split(r"[/\-\s]+", str(texto).strip()) if p]
    if len(partes) not in (2, 3) or not all(p.isdigit() for p in partes):
        return None
    anio = _anio(partes[-1])
    if anio is None or int(partes[0]) == 0:
        return None
    acta = partes[1] if len(partes) == 3 else None
    return int(partes[0]), acta, anio


Resultado = namedtuple("Resultado", "instrumento tipo motivo")
"""instrumento: instancia vinculable (o None); tipo: RES/DEC; motivo: por que no se vinculo."""

NO_PARSEA, SIN_MATCH, AMBIGUO = "no se pudo interpretar", "sin coincidencia", "ambiguo"


def _variantes_acta(acta):
    return {acta, acta.lstrip("0") or "0", acta.zfill(2)}


def _candidatos_resolucion(Resolucion, numero, acta, anio):
    qs = Resolucion.objects.filter(instrumentolegalresoluciones_numero=numero, instrumentolegalresoluciones_ano=anio)
    if acta is None:
        return list(qs.filter(instrumentolegalresoluciones_tipo="P", instrumentolegalresoluciones_acta="")[:2])
    return list(qs.filter(instrumentolegalresoluciones_tipo="D", instrumentolegalresoluciones_acta__in=_variantes_acta(acta))[:2])


def _candidatos_decreto(Decreto, numero, acta, anio):
    if acta is not None:
        return []
    return list(Decreto.objects.filter(
        instrumentolegaldecretos_tipo="P", instrumentolegaldecretos_numero=numero, instrumentolegaldecretos_ano=anio,
    )[:2])


def buscar(tipo, texto, Resolucion=None, Decreto=None):
    """Busca el instrumento que corresponde a un texto heredado.

    - tipo RES: 'n/acta/año' -> Resolucion de Directorio con esa acta; 'n/año' ->
      Resolucion de Presidencia (acta vacia).
    - tipo DEC: 'n/año' -> Decreto Provincial.
    - tipo None: prueba ambos y solo vincula si hay exactamente un candidato en total.
    - Cualquier otro tipo (DIS, ...): no es un instrumento del IPDUV, no se busca.

    Resolucion/Decreto se pueden pasar para usar los modelos historicos de una migracion.
    """
    if Resolucion is None or Decreto is None:
        from secretariador.models import InstrumentosLegalesResoluciones, InstrumentosLegalesDecretos
        Resolucion = Resolucion or InstrumentosLegalesResoluciones
        Decreto = Decreto or InstrumentosLegalesDecretos

    if tipo not in (RES, DEC, None):
        return Resultado(None, None, SIN_MATCH)
    partes = parsear(texto)
    if partes is None:
        return Resultado(None, None, NO_PARSEA)

    candidatos = []
    if tipo in (RES, None):
        candidatos += [(RES, c) for c in _candidatos_resolucion(Resolucion, *partes)]
    if tipo in (DEC, None):
        candidatos += [(DEC, c) for c in _candidatos_decreto(Decreto, *partes)]

    if not candidatos:
        return Resultado(None, None, SIN_MATCH)
    if len(candidatos) > 1:
        return Resultado(None, None, AMBIGUO)
    encontrado_tipo, instrumento = candidatos[0]
    return Resultado(instrumento, encontrado_tipo, None)


def vincular(agente, concepto, Resolucion=None, Decreto=None):
    """Intenta vincular el texto heredado del concepto. Si encuentra el instrumento lo agrega
    a los instrumentos del agente (ver `asignar`, escribe en la base) y vacia el heredado
    (sin guardar el agente). Devuelve (Resultado, campos del agente tocados)."""
    texto = getattr(agente, concepto.heredado)
    if not texto or not (RES in concepto.tipos or DEC in concepto.tipos):
        return None, []
    resultado = buscar(tipo_heredado(agente, concepto), texto, Resolucion, Decreto)
    if resultado.instrumento is None or resultado.tipo not in concepto.tipos:
        if resultado.instrumento is not None:
            resultado = Resultado(None, None, SIN_MATCH)
        return resultado, []
    asignar(agente, concepto, resultado.tipo, resultado.instrumento)
    return resultado, limpiar_heredado(agente, concepto)
