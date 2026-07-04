"""Generación automática de Certificados a partir de una Foja de Medición.

Reglas de negocio implementadas acá (ver plan en /home/willy/.claude/plans):
- Certificado Parcial de Obra: un Certificado por cada financiamiento (ContratoMonto)
  cargado para el Rubro de Certificado vinculado al Rubro del Plan de Trabajos de la Foja,
  aplicando el %mes de la Foja sobre esos montos de contrato.

Esta versión es "naive" en la conversión a pesos cuando el financiamiento tiene
componente en UVI: la Ley 27397 (congelamiento/recuperación de atraso en la cotización
UVI usada) se agrega en `carga.ley27397` sobre esta base, sin cambiar la interfaz pública
de `construir_certificados_desde_foja`/`generar_certificados_desde_foja`.
"""

from decimal import ROUND_HALF_UP, Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q, Sum

from carga import ley27397
from carga.models import Certificado, ContratoMonto, ContratoTramoPago, Uvi

_DOS_DECIMALES = Decimal("0.01")
_TRES_DECIMALES = Decimal("0.001")
_CIEN = Decimal("100")

FINANCIAMIENTO_PREFIJO = {"N": "nacion", "P": "provincia", "T": "terceros"}
TOPE_ANTICIPO_PCT = Decimal("30")


def _redondear_pesos(valor):
    """Los campos monetarios de Certificado son DecimalField(decimal_places=2); los
    cálculos intermedios (a partir de % con 3 decimales) deben redondearse antes de
    asignarse."""
    return (valor or Decimal("0")).quantize(_DOS_DECIMALES, rounding=ROUND_HALF_UP)


def _redondear_pct(valor):
    """Los campos de % de Certificado son DecimalField(decimal_places=3)."""
    return (valor or Decimal("0")).quantize(_TRES_DECIMALES, rounding=ROUND_HALF_UP)


def _serializar_tramos(tramos):
    """Snapshot de auditoría de los tramos usados para certificado_ley27397_detalle."""
    return [
        {
            "etapa_id": tramo.lote.pk,
            "etapa_numero": tramo.lote.etapa_numero,
            "etapa_fecha": tramo.lote.etapa_fecha.isoformat(),
            "pct": str(tramo.pct),
            "tasa_valor": str(tramo.tasa_valor),
            "tasa_fecha": tramo.tasa_fecha.isoformat(),
        }
        for tramo in tramos
    ]


def _validar_plan_vigente(foja):
    if not foja.foja_rubro.rubro_plan.es_vigente():
        raise ValidationError(
            "Sólo se pueden generar certificados a partir del Plan de Trabajos vigente de la obra."
        )


def _contrato_por_etapas(obra):
    """Contrato vigente de `obra`, sólo si está marcado con certificación por etapas
    (esquema de tramos fijos disparados por avance, ver ContratoTramoPago); None si no
    (obra/contrato con el esquema normal de certificados PARCIAL)."""
    contrato = obra.contrato_vigente()
    return contrato if contrato and contrato.contrato_certificacion_por_etapas else None


def financiamientos_de_rubro(foja):
    """ContratoMonto(s) a certificar para el Rubro de Plan de Trabajos de esta Foja.

    Si el rubro tiene `rubro_certificado_rubro` vinculado (rubros financiados por más de
    una fuente a la vez), se usan TODOS los ContratoMonto del Contrato vigente para ese
    Rubro de Certificado (uno por financiamiento). Si no, se usa directamente el
    `rubro_contratomonto` puntual ya vinculado al rubro (caso común, un solo
    financiamiento) — no hace falta cargar nada nuevo para ese caso."""
    rubro = foja.foja_rubro
    rubro_certificado = rubro.rubro_certificado_rubro

    if rubro_certificado is not None:
        obra = rubro.rubro_plan.trabajos_obra
        contrato_vigente = obra.contrato_vigente()
        if contrato_vigente is None:
            raise ValidationError(f"La obra '{obra}' no tiene ningún Contrato cargado.")

        montos = list(
            ContratoMonto.objects.filter(
                contratomonto_contrato=contrato_vigente,
                contratomonto_rubro=rubro_certificado,
            ).select_related("contratomonto_financiamiento")
        )
        if not montos:
            raise ValidationError(
                f"El Contrato vigente de '{obra}' no tiene montos cargados para el rubro '{rubro_certificado}'."
            )
        return montos

    if rubro.rubro_contratomonto_id:
        return [rubro.rubro_contratomonto]

    raise ValidationError(
        f"El rubro '{rubro.rubro_nombre}' del Plan de Trabajos no tiene ningún monto de "
        "contrato vinculado (ni un Monto de Contrato puntual, ni un Rubro de Certificado)."
    )


def siguiente_numero(obra, financiamiento, tipo):
    """Correlativo de certificado dentro de una serie (obra + financiamiento + tipo)."""
    return (
        Certificado.objects.filter(
            certificado_obra=obra, certificado_financiamiento=financiamiento, certificado_tipo=tipo
        ).count()
        + 1
    )


def _monto_contrato_financiamiento(obra, financiamiento_codigo, moneda):
    prefijo = FINANCIAMIENTO_PREFIJO[financiamiento_codigo]
    return getattr(obra, f"obra_contrato_{prefijo}_{moneda}") or Decimal("0")


def _monto_contrato_rubro(certificado):
    """Monto de contrato (pesos, uvi) del Contrato/Rubro que `certificado` realmente
    certifica: el Contrato de origen si es un Hecho Consumado, o el vigente de la obra si
    no (PARCIAL/ANTICIPO). Es la base correcta para expresar el % de avance de un
    certificado puntual — a diferencia de `_monto_contrato_financiamiento`, que suma TODOS
    los rubros/contratos de la obra para ese financiamiento y sólo debe usarse para la
    lógica de pool de anticipos (obra+financiamiento, no por rubro)."""
    obra = certificado.certificado_obra
    contrato = certificado.certificado_contrato_origen or obra.contrato_vigente()
    if contrato is None:
        return Decimal("0"), Decimal("0")
    contratomonto = ContratoMonto.objects.filter(
        contratomonto_contrato=contrato,
        contratomonto_rubro=certificado.certificado_rubro_db,
        contratomonto_financiamiento__certificadofinanciamiento_nombre_corto=certificado.certificado_financiamiento,
    ).first()
    if contratomonto is None:
        return Decimal("0"), Decimal("0")
    return contratomonto.contratomonto_pesos, contratomonto.contratomonto_uvi


def _certificados_obra_financiamiento(obra, financiamiento_codigo, excluir_pk=None):
    qs = Certificado.objects.filter(certificado_obra=obra, certificado_financiamiento=financiamiento_codigo)
    if excluir_pk:
        qs = qs.exclude(pk=excluir_pk)
    return qs


def _saldo_pendiente_anticipo(obra, financiamiento_codigo, moneda, excluir_pk=None):
    """Saldo pendiente de anticipo en la unidad `moneda` (pesos o uvi), pool único por
    obra+financiamiento: lo otorgado (certificados ANTICIPO nuevos + legacy marcados con
    certificado_rubro_anticipo>0) menos lo ya devuelto/descontado (devoluciones legacy +
    descuentos automáticos ya aplicados en certificados PARCIAL/HECHO_CONSUMADO)."""
    campo_monto = "certificado_monto_uvi" if moneda == "uvi" else "certificado_monto_pesos"
    campo_devolucion = "certificado_devolucion_monto_uvi" if moneda == "uvi" else "certificado_devolucion_monto"
    campo_descuento = "certificado_descuento_anticipo_uvi" if moneda == "uvi" else "certificado_descuento_anticipo_pesos"

    certificados = _certificados_obra_financiamiento(obra, financiamiento_codigo, excluir_pk)

    otorgado = certificados.filter(Q(certificado_tipo="ANTICIPO") | Q(certificado_rubro_anticipo__gt=0)).aggregate(
        total=Sum(campo_monto)
    )["total"] or Decimal("0")
    devuelto = certificados.filter(certificado_rubro_devanticipo__gt=0).aggregate(total=Sum(campo_devolucion))[
        "total"
    ] or Decimal("0")
    descontado = certificados.filter(certificado_tipo__in=("PARCIAL", "HECHO_CONSUMADO")).aggregate(
        total=Sum(campo_descuento)
    )["total"] or Decimal("0")

    return otorgado - devuelto - descontado


def _saldo_a_certificar(obra, financiamiento_codigo, moneda, excluir_pk=None):
    """Monto de contrato aún no certificado para este financiamiento (certificados
    PARCIAL/HECHO_CONSUMADO nuevos + legacy marcados con certificado_rubro_obra>0)."""
    campo_monto = "certificado_monto_uvi" if moneda == "uvi" else "certificado_monto_pesos"
    certificados = _certificados_obra_financiamiento(obra, financiamiento_codigo, excluir_pk)

    ya_certificado = certificados.filter(
        Q(certificado_tipo__in=("PARCIAL", "HECHO_CONSUMADO")) | Q(certificado_rubro_obra__gt=0)
    ).aggregate(total=Sum(campo_monto))["total"] or Decimal("0")

    return _monto_contrato_financiamiento(obra, financiamiento_codigo, moneda) - ya_certificado


def _tasa_descuento(saldo_pendiente, saldo_a_certificar):
    if not saldo_pendiente or saldo_pendiente <= 0:
        return Decimal("0")
    if not saldo_a_certificar or saldo_a_certificar <= 0:
        return Decimal("1")
    return min(saldo_pendiente / saldo_a_certificar, Decimal("1"))


def aplicar_descuento_anticipo(certificado):
    """Calcula el descuento de anticipo de `certificado` (PARCIAL o HECHO_CONSUMADO) y lo
    asigna in-place, sobre el monto bruto ya resuelto (Ley 27397 u hecho consumado). El
    anticipo se amortiza dinámicamente: la tasa de descuento de cada certificado es
    saldo_pendiente_de_anticipos / saldo_a_certificar_de_ese_financiamiento, recalculada en
    cada certificado nuevo. Un certificado ANTICIPO nunca se descuenta a sí mismo."""
    obra = certificado.certificado_obra
    financiamiento = certificado.certificado_financiamiento
    excluir_pk = certificado.pk

    saldo_pendiente_pesos = _saldo_pendiente_anticipo(obra, financiamiento, "pesos", excluir_pk)
    saldo_pendiente_uvi = _saldo_pendiente_anticipo(obra, financiamiento, "uvi", excluir_pk)
    saldo_a_certificar_pesos = _saldo_a_certificar(obra, financiamiento, "pesos", excluir_pk)
    saldo_a_certificar_uvi = _saldo_a_certificar(obra, financiamiento, "uvi", excluir_pk)

    monto_bruto_pesos = certificado.certificado_monto_pesos or Decimal("0")
    monto_bruto_uvi = certificado.certificado_monto_uvi or Decimal("0")

    tasa_pesos = _tasa_descuento(saldo_pendiente_pesos, saldo_a_certificar_pesos)
    tasa_uvi = _tasa_descuento(saldo_pendiente_uvi, saldo_a_certificar_uvi)

    certificado.certificado_descuento_anticipo_pesos = _redondear_pesos(
        min(monto_bruto_pesos * tasa_pesos, max(saldo_pendiente_pesos, Decimal("0")))
    )
    certificado.certificado_descuento_anticipo_uvi = _redondear_pesos(
        min(monto_bruto_uvi * tasa_uvi, max(saldo_pendiente_uvi, Decimal("0")))
    )

    # % efectivo (post-tope) del monto bruto que efectivamente se retuvo, en la misma
    # moneda "real" del certificado (UVI si el financiamiento tiene componente UVI, si no
    # pesos) — mismo criterio que usa _fila_resumen para elegir moneda.
    if monto_bruto_uvi:
        certificado.certificado_descuento_anticipo_pct = _redondear_pct(
            certificado.certificado_descuento_anticipo_uvi / monto_bruto_uvi * _CIEN
        )
    elif monto_bruto_pesos:
        certificado.certificado_descuento_anticipo_pct = _redondear_pct(
            certificado.certificado_descuento_anticipo_pesos / monto_bruto_pesos * _CIEN
        )
    else:
        certificado.certificado_descuento_anticipo_pct = Decimal("0")

    # Numeración correlativa "Dev. N°" (misma convención que usaban los certificados
    # legacy marcados a mano): sólo se asigna cuando efectivamente hay descuento.
    if certificado.certificado_descuento_anticipo_pesos or certificado.certificado_descuento_anticipo_uvi:
        certificado.certificado_rubro_devanticipo = (
            Certificado.objects.filter(
                certificado_obra=obra, certificado_financiamiento=financiamiento, certificado_rubro_devanticipo__gt=0
            )
            .exclude(pk=excluir_pk)
            .count()
            + 1
        )


def calcular_monto_anticipo(certificado):
    """Deriva certificado_monto_uvi/certificado_monto_pesos de un Certificado ANTICIPO a
    partir de certificado_anticipo_pct (cargado a mano): si
    el financiamiento tiene componente UVI, convierte a pesos con la cotización del día de
    creación del certificado (no la pactada del contrato ni la de fin de mes: el Anticipo
    no tiene Foja/Etapa detrás, no le aplica ningún tramo de Ley 27397); si no, calcula
    pesos directo sobre el monto de contrato en pesos."""
    obra = certificado.certificado_obra
    financiamiento = certificado.certificado_financiamiento
    pct = certificado.certificado_anticipo_pct or Decimal("0")

    base_uvi = _monto_contrato_financiamiento(obra, financiamiento, "uvi")
    if base_uvi:
        monto_uvi = _redondear_pesos(base_uvi * pct / _CIEN)
        monto_pesos = Uvi.pesos_equivalentes(monto_uvi, certificado.certificado_fecha)
        if monto_pesos is None:
            raise ValidationError(
                "No hay cotización UVI disponible para la fecha del certificado; no se puede "
                "convertir el anticipo a pesos."
            )
        certificado.certificado_monto_uvi = monto_uvi
        certificado.certificado_monto_pesos = _redondear_pesos(monto_pesos)
    else:
        base_pesos = _monto_contrato_financiamiento(obra, financiamiento, "pesos")
        certificado.certificado_monto_uvi = Decimal("0")
        certificado.certificado_monto_pesos = _redondear_pesos(base_pesos * pct / _CIEN)


def validar_anticipo_nuevo(obra, financiamiento, pct_nuevo):
    """Valida los dos topes de un Anticipo nuevo:
    1) el saldo pendiente de anticipo (lo ya otorgado, neto de lo devuelto/descontado) más
       este nuevo anticipo no puede superar el 30% del monto de contrato del financiamiento
       (lo ya devuelto/descontado no cuenta contra este tope).
    2) tiene que haber margen suficiente en el saldo de contrato aún no certificado para
       poder recuperar ese anticipo (si no, nunca terminaría de descontarse).
    Se chequea en UVI si el financiamiento tiene componente UVI, en pesos si no."""
    pct_nuevo = pct_nuevo or Decimal("0")
    moneda = "uvi" if _monto_contrato_financiamiento(obra, financiamiento, "uvi") else "pesos"
    base = _monto_contrato_financiamiento(obra, financiamiento, moneda)
    if not base:
        raise ValidationError("La obra no tiene monto de contrato cargado para este financiamiento.")

    saldo_pendiente = _saldo_pendiente_anticipo(obra, financiamiento, moneda)
    nuevo_monto = base * pct_nuevo / _CIEN
    nuevo_saldo_pendiente = saldo_pendiente + nuevo_monto

    if (nuevo_saldo_pendiente / base) * _CIEN > TOPE_ANTICIPO_PCT:
        raise ValidationError(
            f"El anticipo pendiente de esta obra no puede superar el {TOPE_ANTICIPO_PCT}% del "
            "monto de contrato (lo ya devuelto/descontado no cuenta contra este tope)."
        )

    saldo_a_certificar = _saldo_a_certificar(obra, financiamiento, moneda)
    if nuevo_saldo_pendiente > saldo_a_certificar:
        raise ValidationError("No hay saldo de contrato suficiente para poder recuperar este anticipo.")


def calcular_monto_hecho_consumado(certificado):
    """Deriva certificado_monto_uvi/certificado_monto_pesos de un Certificado
    HECHO_CONSUMADO: % cargado a mano (certificado_mes_pct) aplicado sobre el ContratoMonto
    de certificado_contrato_origen para su Rubro/Financiamiento, convirtiendo a pesos con la
    cotización UVI de certificado_fecha (misma convención que calcular_monto_anticipo): sin
    Foja/Etapa de por medio no aplica la lógica de atraso de Ley 27397, y usar la cotización
    pactada del contrato subvaluaría el certificado si quedó firmado mucho antes de emitirse."""
    pct = certificado.certificado_mes_pct or Decimal("0")
    contratomonto = ContratoMonto.objects.filter(
        contratomonto_contrato=certificado.certificado_contrato_origen,
        contratomonto_rubro=certificado.certificado_rubro_db,
        contratomonto_financiamiento__certificadofinanciamiento_nombre_corto=certificado.certificado_financiamiento,
    ).first()
    if contratomonto is None:
        raise ValidationError(
            "El Contrato de origen no tiene un monto cargado para este Rubro y Financiamiento."
        )

    if contratomonto.contratomonto_uvi:
        monto_uvi = _redondear_pesos(contratomonto.contratomonto_uvi * pct / _CIEN)
        monto_pesos = Uvi.pesos_equivalentes(monto_uvi, certificado.certificado_fecha)
        if monto_pesos is None:
            raise ValidationError(
                "No hay cotización UVI disponible para la fecha del certificado; no se puede "
                "convertir el Hecho Consumado a pesos."
            )
        certificado.certificado_monto_uvi = monto_uvi
        certificado.certificado_monto_pesos = _redondear_pesos(monto_pesos)
    else:
        certificado.certificado_monto_uvi = Decimal("0")
        certificado.certificado_monto_pesos = _redondear_pesos(contratomonto.contratomonto_pesos * pct / _CIEN)


def _corte_certificados(obra, financiamiento_codigo, fecha, pk, tipos=None, hasta_incluir=True):
    """Certificados de `obra`+`financiamiento_codigo` hasta el corte (fecha, pk) —
    mismo orden que `Certificado.Meta.ordering`. `hasta_incluir=True` incluye el
    propio certificado (fecha, pk); False lo excluye (para el "acumulado anterior")."""
    qs = Certificado.objects.filter(certificado_obra=obra, certificado_financiamiento=financiamiento_codigo)
    if tipos:
        qs = qs.filter(certificado_tipo__in=tipos)
    if hasta_incluir:
        return qs.filter(Q(certificado_fecha__lt=fecha) | Q(certificado_fecha=fecha, pk__lte=pk))
    return qs.filter(Q(certificado_fecha__lt=fecha) | Q(certificado_fecha=fecha, pk__lt=pk))


def _suma(qs, campo_pesos, campo_uvi):
    agregado = qs.aggregate(pesos=Sum(campo_pesos), uvi=Sum(campo_uvi))
    return agregado["pesos"] or Decimal("0"), agregado["uvi"] or Decimal("0")


def _fila_resumen(etiqueta, total_pesos, total_uvi, anterior_pesos, anterior_uvi, base_pesos, base_uvi, con_pct=True):
    fila = {
        "etiqueta": etiqueta,
        "mes_pesos": _redondear_pesos(total_pesos - anterior_pesos),
        "mes_uvi": _redondear_pesos(total_uvi - anterior_uvi),
        "anterior_pesos": _redondear_pesos(anterior_pesos),
        "anterior_uvi": _redondear_pesos(anterior_uvi),
        "total_pesos": _redondear_pesos(total_pesos),
        "total_uvi": _redondear_pesos(total_uvi),
    }
    # La obra puede estar financiada en UVI o directamente en pesos (sin componente
    # UVI): "mes"/"anterior"/"total" exponen el valor en la moneda que corresponda,
    # para que la plantilla no tenga que decidir entre *_pesos/*_uvi fila por fila.
    if base_uvi:
        fila["mes"], fila["anterior"], fila["total"] = fila["mes_uvi"], fila["anterior_uvi"], fila["total_uvi"]
    else:
        fila["mes"], fila["anterior"], fila["total"] = fila["mes_pesos"], fila["anterior_pesos"], fila["total_pesos"]
    if con_pct:
        base = base_uvi or base_pesos
        fila["mes_pct"], fila["anterior_pct"], fila["total_pct"] = (
            (_redondear_pct(valor / base * _CIEN) if base else Decimal("0"))
            for valor in (fila["mes"], fila["anterior"], fila["total"])
        )
    return fila


def resumen_certificacion_mensual(certificado):
    """Resumen mensual de la certificación (nota de elevación IPDUV): para el mismo
    obra+financiamiento de `certificado`, cuánto corresponde a este mes / lo
    acumulado anterior / el acumulado total, separado en Certificado de Obra,
    Anticipo, Devolución de Anticipo, Subtotal 1, Fondo de Reparo y Total General. Los %
    se expresan contra el monto de contrato del Rubro que `certificado` certifica (ver
    `_monto_contrato_rubro`), no contra el total de la obra (que puede sumar varios
    rubros/contratos bajo el mismo financiamiento, p.ej. un Hecho Consumado de
    Reconocimiento de Trabajos aparte del contrato de Vivienda). Excepción: Anticipo y
    Devolución de Anticipo se calculan y validan (ver aplicar_descuento_anticipo,
    validar_anticipo_nuevo) contra el pool de TODOS los rubros/contratos de la obra para
    ese financiamiento (`_monto_contrato_financiamiento`), no contra un rubro puntual —
    esas dos filas usan esa base en vez de `_monto_contrato_rubro` para que su % sea
    consistente con cómo se calcularon esos montos. Certificado de Etapa (obras con
    Contrato marcado por etapas) usa a su vez su propia base, el Contrato completo
    (`_monto_contrato_total`, ver calcular_monto_etapa) — nunca convive con Certificado de
    Obra/Anticipo/Devolución en la misma obra, pero de existir todas se suman igual en
    Subtotal 1 y Fondo de Reparo."""
    obra = certificado.certificado_obra
    financiamiento = certificado.certificado_financiamiento
    fecha, pk = certificado.certificado_fecha, certificado.pk

    base_pesos, base_uvi = _monto_contrato_rubro(certificado)
    base_pool_pesos = _monto_contrato_financiamiento(obra, financiamiento, "pesos")
    base_pool_uvi = _monto_contrato_financiamiento(obra, financiamiento, "uvi")

    # La fila de Etapa usa su propia base (el Contrato completo marcado por etapas, no el
    # rubro puntual de `_monto_contrato_rubro` ni el pool histórico de
    # `_monto_contrato_financiamiento`): mismo criterio que calcular_monto_etapa.
    contrato_etapas = _contrato_por_etapas(obra)
    if contrato_etapas:
        base_etapa_pesos = _monto_contrato_total(contrato_etapas, financiamiento, "pesos")
        base_etapa_uvi = _monto_contrato_total(contrato_etapas, financiamiento, "uvi")
    else:
        base_etapa_pesos = base_etapa_uvi = Decimal("0")

    obra_total_qs = _corte_certificados(obra, financiamiento, fecha, pk, tipos=("PARCIAL", "HECHO_CONSUMADO"))
    obra_anterior_qs = _corte_certificados(obra, financiamiento, fecha, pk, tipos=("PARCIAL", "HECHO_CONSUMADO"), hasta_incluir=False)
    obra_total_pesos, obra_total_uvi = _suma(obra_total_qs, "certificado_monto_pesos", "certificado_monto_uvi")
    obra_anterior_pesos, obra_anterior_uvi = _suma(obra_anterior_qs, "certificado_monto_pesos", "certificado_monto_uvi")
    fila_obra = _fila_resumen(
        "Certificado de Obra", obra_total_pesos, obra_total_uvi, obra_anterior_pesos, obra_anterior_uvi, base_pesos, base_uvi
    )

    anticipo_total_qs = _corte_certificados(obra, financiamiento, fecha, pk, tipos=("ANTICIPO",))
    anticipo_anterior_qs = _corte_certificados(obra, financiamiento, fecha, pk, tipos=("ANTICIPO",), hasta_incluir=False)
    anticipo_total_pesos, anticipo_total_uvi = _suma(anticipo_total_qs, "certificado_monto_pesos", "certificado_monto_uvi")
    anticipo_anterior_pesos, anticipo_anterior_uvi = _suma(anticipo_anterior_qs, "certificado_monto_pesos", "certificado_monto_uvi")
    fila_anticipo = _fila_resumen(
        "Anticipo", anticipo_total_pesos, anticipo_total_uvi, anticipo_anterior_pesos, anticipo_anterior_uvi,
        base_pool_pesos, base_pool_uvi
    )

    def _devolucion(qs_obra, qs_legacy):
        descuento_pesos, descuento_uvi = _suma(qs_obra, "certificado_descuento_anticipo_pesos", "certificado_descuento_anticipo_uvi")
        legacy_pesos, legacy_uvi = _suma(qs_legacy, "certificado_devolucion_monto", "certificado_devolucion_monto_uvi")
        return descuento_pesos + legacy_pesos, descuento_uvi + legacy_uvi

    legacy_total_qs = _corte_certificados(obra, financiamiento, fecha, pk).filter(certificado_rubro_devanticipo__gt=0)
    legacy_anterior_qs = _corte_certificados(obra, financiamiento, fecha, pk, hasta_incluir=False).filter(certificado_rubro_devanticipo__gt=0)
    devolucion_total_pesos, devolucion_total_uvi = _devolucion(obra_total_qs, legacy_total_qs)
    devolucion_anterior_pesos, devolucion_anterior_uvi = _devolucion(obra_anterior_qs, legacy_anterior_qs)
    fila_devolucion = _fila_resumen(
        "Devolución de Anticipo", devolucion_total_pesos, devolucion_total_uvi,
        devolucion_anterior_pesos, devolucion_anterior_uvi, base_pool_pesos, base_pool_uvi
    )

    etapa_total_qs = _corte_certificados(obra, financiamiento, fecha, pk, tipos=("ETAPA",))
    etapa_anterior_qs = _corte_certificados(obra, financiamiento, fecha, pk, tipos=("ETAPA",), hasta_incluir=False)
    etapa_total_pesos, etapa_total_uvi = _suma(etapa_total_qs, "certificado_monto_pesos", "certificado_monto_uvi")
    etapa_anterior_pesos, etapa_anterior_uvi = _suma(etapa_anterior_qs, "certificado_monto_pesos", "certificado_monto_uvi")
    fila_etapa = _fila_resumen(
        "Certificado de Etapa", etapa_total_pesos, etapa_total_uvi, etapa_anterior_pesos, etapa_anterior_uvi,
        base_etapa_pesos, base_etapa_uvi
    )

    subtotal_total_pesos = obra_total_pesos + etapa_total_pesos + anticipo_total_pesos - devolucion_total_pesos
    subtotal_total_uvi = obra_total_uvi + etapa_total_uvi + anticipo_total_uvi - devolucion_total_uvi
    subtotal_anterior_pesos = obra_anterior_pesos + etapa_anterior_pesos + anticipo_anterior_pesos - devolucion_anterior_pesos
    subtotal_anterior_uvi = obra_anterior_uvi + etapa_anterior_uvi + anticipo_anterior_uvi - devolucion_anterior_uvi
    fila_subtotal = _fila_resumen(
        "Subtotal 1", subtotal_total_pesos, subtotal_total_uvi, subtotal_anterior_pesos, subtotal_anterior_uvi, base_pesos, base_uvi
    )

    def _fondo_reparo(qs):
        pesos = uvi = Decimal("0")
        for c in qs:
            pesos += c.certificado_fondoreparo_monto_pesos()
            uvi += c.certificado_fondoreparo_monto_uvi()
        return pesos, uvi

    fondo_obra_total_pesos, fondo_obra_total_uvi = _fondo_reparo(obra_total_qs)
    fondo_obra_anterior_pesos, fondo_obra_anterior_uvi = _fondo_reparo(obra_anterior_qs)
    fondo_etapa_total_pesos, fondo_etapa_total_uvi = _fondo_reparo(etapa_total_qs)
    fondo_etapa_anterior_pesos, fondo_etapa_anterior_uvi = _fondo_reparo(etapa_anterior_qs)
    fondo_total_pesos = fondo_obra_total_pesos + fondo_etapa_total_pesos
    fondo_total_uvi = fondo_obra_total_uvi + fondo_etapa_total_uvi
    fondo_anterior_pesos = fondo_obra_anterior_pesos + fondo_etapa_anterior_pesos
    fondo_anterior_uvi = fondo_obra_anterior_uvi + fondo_etapa_anterior_uvi
    fila_fondo = _fila_resumen(
        "Fondo de Reparo", fondo_total_pesos, fondo_total_uvi, fondo_anterior_pesos, fondo_anterior_uvi,
        base_pesos, base_uvi, con_pct=False
    )

    total_general_total_pesos = subtotal_total_pesos - fondo_total_pesos
    total_general_total_uvi = subtotal_total_uvi - fondo_total_uvi
    total_general_anterior_pesos = subtotal_anterior_pesos - fondo_anterior_pesos
    total_general_anterior_uvi = subtotal_anterior_uvi - fondo_anterior_uvi
    fila_total_general = _fila_resumen(
        "Total General", total_general_total_pesos, total_general_total_uvi,
        total_general_anterior_pesos, total_general_anterior_uvi, base_pesos, base_uvi, con_pct=False
    )

    return {
        "unidad": "UVI" if base_uvi else "$",
        "filas": [fila_obra, fila_etapa, fila_anticipo, fila_devolucion, fila_subtotal, fila_fondo, fila_total_general],
        "certificado_obra": fila_obra,
        "etapa": fila_etapa,
        "anticipo": fila_anticipo,
        "devolucion": fila_devolucion,
        "subtotal1": fila_subtotal,
        "fondo_reparo": fila_fondo,
        "total_general": fila_total_general,
    }


def _monto_contrato_total(contrato, financiamiento_codigo, moneda):
    """Suma de todos los ContratoMonto de `contrato` para `financiamiento_codigo` (todos
    los rubros que financia), en la unidad `moneda`. Base de los tramos de pago por etapas,
    que son un esquema a nivel de Contrato completo, no de un Rubro puntual (a diferencia
    de `_monto_contrato_rubro`)."""
    campo = "contratomonto_uvi" if moneda == "uvi" else "contratomonto_pesos"
    return ContratoMonto.objects.filter(
        contratomonto_contrato=contrato,
        contratomonto_financiamiento__certificadofinanciamiento_nombre_corto=financiamiento_codigo,
    ).aggregate(total=Sum(campo))["total"] or Decimal("0")


def calcular_monto_etapa(certificado):
    """Deriva certificado_monto_uvi/certificado_monto_pesos de un Certificado ETAPA: el %
    fijo del tramo (certificado_contrato_tramo.tramo_pct_pago) aplicado sobre el monto TOTAL
    del Contrato para este financiamiento (todos los rubros que financia: el esquema de
    tramos es un cronograma de pago a nivel de Contrato completo, no de un Rubro puntual),
    convertido a pesos con la cotización UVI de certificado_fecha -- misma convención que
    calcular_monto_anticipo/calcular_monto_hecho_consumado: un tramo es un % fijo pactado
    que no depende del avance real del mes, por lo que no le aplica ningún tramo de Ley
    27397."""
    tramo = certificado.certificado_contrato_tramo
    contrato = tramo.tramo_contrato
    financiamiento = certificado.certificado_financiamiento
    pct = tramo.tramo_pct_pago

    base_uvi = _monto_contrato_total(contrato, financiamiento, "uvi")
    if base_uvi:
        monto_uvi = _redondear_pesos(base_uvi * pct / _CIEN)
        monto_pesos = Uvi.pesos_equivalentes(monto_uvi, certificado.certificado_fecha)
        if monto_pesos is None:
            raise ValidationError(
                "No hay cotización UVI disponible para la fecha del certificado; no se puede "
                "convertir el Certificado de Etapa a pesos."
            )
        certificado.certificado_monto_uvi = monto_uvi
        certificado.certificado_monto_pesos = _redondear_pesos(monto_pesos)
    else:
        base_pesos = _monto_contrato_total(contrato, financiamiento, "pesos")
        certificado.certificado_monto_uvi = Decimal("0")
        certificado.certificado_monto_pesos = _redondear_pesos(base_pesos * pct / _CIEN)


def _construir_certificados_etapa(
    foja, contrato, certificado_expediente, certificado_fecha, certificado_fecha_carga_legacy
):
    """Devuelve, sin persistir nada, los Certificado ETAPA (uno por cada tramo de pago del
    Contrato que la Foja haya habilitado y todavía no esté certificado, por cada
    financiamiento del Contrato) que se generarían para esta Foja. Una Foja puede habilitar
    más de un tramo de una sola vez si el avance salta de golpe más de un umbral."""
    acum_pct = _redondear_pct(foja.foja_pct_acumulado())
    mes_pct = _redondear_pct(foja.foja_pct_avance_mes())
    ante_pct = acum_pct - mes_pct

    financiamientos = sorted({
        cm.contratomonto_financiamiento.certificadofinanciamiento_nombre_corto
        for cm in ContratoMonto.objects.filter(contratomonto_contrato=contrato).select_related(
            "contratomonto_financiamiento"
        )
    })
    if not financiamientos:
        raise ValidationError(f"El Contrato '{contrato}' no tiene ningún monto cargado.")

    rubro = foja.foja_rubro
    rubro_certificado = rubro.rubro_certificado_rubro or (
        rubro.rubro_contratomonto.contratomonto_rubro if rubro.rubro_contratomonto_id else None
    )
    if rubro_certificado is None:
        raise ValidationError(
            f"El rubro '{rubro.rubro_nombre}' del Plan de Trabajos no tiene ningún Rubro de "
            "Certificado vinculado."
        )

    certificados = []
    for financiamiento in financiamientos:
        tramos_pendientes = ContratoTramoPago.objects.filter(
            tramo_contrato=contrato, certificado_etapa__isnull=True, tramo_pct_disparador__lte=acum_pct
        ).order_by("tramo_numero")
        for tramo in tramos_pendientes:
            certificado = Certificado(
                certificado_obra=contrato.contrato_obra,
                certificado_tipo="ETAPA",
                certificado_foja=foja,
                certificado_contrato_tramo=tramo,
                certificado_financiamiento=financiamiento,
                certificado_rubro_db=rubro_certificado,
                certificado_rubro_obra=tramo.tramo_numero,
                certificado_expediente=certificado_expediente,
                certificado_fecha=certificado_fecha,
                certificado_mes_pct=mes_pct,
                certificado_ante_pct=ante_pct,
                certificado_acum_pct=acum_pct,
                certificado_etapa_pct=tramo.tramo_pct_pago,
                certificado_fecha_carga_legacy=certificado_fecha_carga_legacy,
            )
            calcular_monto_etapa(certificado)
            certificado.full_clean()
            certificados.append(certificado)
    return certificados


def construir_certificados_desde_foja(
    foja, certificado_expediente, certificado_fecha, certificado_fecha_carga_legacy=False
):
    """Devuelve, sin persistir nada, los Certificado PARCIAL (uno por financiamiento del
    rubro de la Foja) que se generarían para esta Foja. Útil tanto para previsualizar como
    para guardar (ver generar_certificados_desde_foja).

    Si el Contrato vigente de la obra está marcado con certificación por etapas, arma en
    cambio Certificado(s) ETAPA (ver _construir_certificados_etapa) -- ambos esquemas son
    excluyentes entre sí."""
    _validar_plan_vigente(foja)
    obra = foja.foja_rubro.rubro_plan.trabajos_obra
    contrato_etapas = _contrato_por_etapas(obra)
    if contrato_etapas:
        return _construir_certificados_etapa(
            foja, contrato_etapas, certificado_expediente, certificado_fecha, certificado_fecha_carga_legacy
        )

    montos = financiamientos_de_rubro(foja)

    obra = foja.foja_rubro.rubro_plan.trabajos_obra
    mes_pct = _redondear_pct(foja.foja_pct_avance_mes())
    acum_pct = _redondear_pct(foja.foja_pct_acumulado())
    ante_pct = acum_pct - mes_pct

    certificados = []
    for contratomonto in montos:
        financiamiento = contratomonto.contratomonto_financiamiento.certificadofinanciamiento_nombre_corto
        ley27397_detalle = None

        if contratomonto.contratomonto_uvi:
            # Financiamiento con componente UVI: Ley 27397 rige la cotización usada para
            # convertir a pesos (el monto en UVI en sí no tiene lógica de atraso).
            tramos = ley27397.resolver_tasas_periodo(foja, contratomonto.contratomonto_financiamiento)
            monto_pesos = _redondear_pesos(ley27397.tramos_a_pesos(tramos, contratomonto.contratomonto_financiamiento))
            monto_uvi = _redondear_pesos(ley27397.certificado_monto_uvi_foja(foja, contratomonto))
            ley27397_detalle = _serializar_tramos(tramos)
        else:
            # Sin componente UVI: cálculo naive, Ley 27397 no aplica en absoluto.
            monto_pesos = _redondear_pesos(contratomonto.contratomonto_pesos * mes_pct / Decimal("100"))
            monto_uvi = Decimal("0")

        certificado = Certificado(
            certificado_obra=obra,
            certificado_tipo="PARCIAL",
            certificado_foja=foja,
            certificado_financiamiento=financiamiento,
            certificado_rubro_db=contratomonto.contratomonto_rubro,
            certificado_rubro_obra=siguiente_numero(obra, financiamiento, "PARCIAL"),
            certificado_expediente=certificado_expediente,
            certificado_fecha=certificado_fecha,
            certificado_mes_pct=mes_pct,
            certificado_ante_pct=ante_pct,
            certificado_acum_pct=acum_pct,
            certificado_monto_pesos=monto_pesos,
            certificado_monto_uvi=monto_uvi,
            certificado_ley27397_detalle=ley27397_detalle,
            certificado_fecha_carga_legacy=certificado_fecha_carga_legacy,
        )
        aplicar_descuento_anticipo(certificado)
        certificado.full_clean()
        certificados.append(certificado)
    return certificados


def generar_certificados_desde_foja(
    foja, certificado_expediente, certificado_fecha, certificado_fecha_carga_legacy=False
):
    """Construye y persiste los certificados de construir_certificados_desde_foja, todo o nada."""
    certificados = construir_certificados_desde_foja(
        foja, certificado_expediente, certificado_fecha, certificado_fecha_carga_legacy
    )
    with transaction.atomic():
        for certificado in certificados:
            certificado.save()
    return certificados
