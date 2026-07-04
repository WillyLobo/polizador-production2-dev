"""Ley 27397: resolución de la cotización UVI->$ aplicable a cada tramo de avance
certificado, respetando el mecanismo de "congelamiento"/recuperación de atraso (art. 2°).

El test de cumplimiento del 90% (art. 2°) se hace a nivel de Rubro completo (no por
item): sólo importa el avance físico total, para no penalizar que la empresa acelere
unos items y postergue otros.

El test del 90% de un lote (mes proyectado) se reevalúa en CADA abono que lo toca, no
sólo en el primero: un lote recién congela su cotización "propia" (la de fin de mes de
su propio período) el abono en el que efectivamente alcanza su 90% acumulado proyectado;
hasta entonces, cada abono a ese lote usa la cotización vigente heredada del último lote
resuelto (o la pactada del ContratoMonto, si es el primer lote de toda la cadena y todavía
no hay ninguna cotización vigente).

Un Rubro de Plan de Trabajos puede tener contrato en varios financiamientos a la vez
(Nación + Provincia simultáneos), por lo que las funciones acá reciben explícitamente
el financiamiento/ContratoMonto sobre el que se está certificando.
"""

import calendar
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from carga.models import ContratoMonto, FojaDeMedicion, PlanDeTrabajosEtapa, Uvi


class Ley27397Error(Exception):
    pass


class SinProyeccionError(Ley27397Error):
    def __init__(self, rubro):
        self.rubro = rubro
        super().__init__(f"El rubro '{rubro}' no tiene ninguna Etapa proyectada cargada.")


class ProyeccionInsuficienteError(Ley27397Error):
    def __init__(self, rubro, sobrante_pct):
        self.rubro = rubro
        self.sobrante_pct = sobrante_pct
        super().__init__(
            f"El avance real de '{rubro}' supera todo lo proyectado cargado "
            f"(sobra {sobrante_pct}% sin Etapa que lo respalde)."
        )


class SinMontoBaseUviError(Ley27397Error):
    def __init__(self, lote):
        self.lote = lote
        super().__init__(
            f"La Etapa '{lote}' no tiene un monto en UVI cargado para este financiamiento."
        )


class SinTasaContratoError(Ley27397Error):
    def __init__(self, contratomonto):
        self.contratomonto = contratomonto
        super().__init__(
            f"El Contrato '{contratomonto}' no tiene una fecha de cotización UVI pactada "
            "(contratomonto_uvi_fecha)."
        )


class CotizacionFaltanteError(Ley27397Error):
    def __init__(self, fecha_mes):
        self.fecha_mes = fecha_mes
        super().__init__(
            f"No hay cotización UVI cargada para el {fecha_mes} (el sincronizador bcra_uvi "
            "puede no haber llegado todavía a esa fecha)."
        )


@dataclass(frozen=True)
class TramoResuelto:
    pct: Decimal
    tasa_valor: Decimal
    tasa_fecha: date
    lote: "PlanDeTrabajosEtapa"


def fin_de_mes(fecha_mes):
    ultimo_dia = calendar.monthrange(fecha_mes.year, fecha_mes.month)[1]
    return fecha_mes.replace(day=ultimo_dia)


def cotizacion_fin_de_mes(fecha_mes):
    """A diferencia de Uvi.pesos_equivalentes, la ley exige puntualmente el valor del
    último día calendario del mes: no tolera la cotización más cercana anterior."""
    fecha = fin_de_mes(fecha_mes)
    uvi = Uvi.objects.filter(uvi_fecha=fecha).first()
    if uvi is None:
        raise CotizacionFaltanteError(fecha)
    return uvi.uvi_valor


def tasa_contrato(contratomonto):
    """Cotización UVI pactada de un ContratoMonto (tolera la cotización más cercana
    anterior, vía Uvi.pesos_equivalentes, a diferencia de cotizacion_fin_de_mes)."""
    if not contratomonto or not contratomonto.contratomonto_uvi_fecha:
        raise SinTasaContratoError(contratomonto)
    tasa = Uvi.pesos_equivalentes(Decimal("1"), contratomonto.contratomonto_uvi_fecha)
    if tasa is None:
        raise CotizacionFaltanteError(contratomonto.contratomonto_uvi_fecha)
    return tasa


def _contratomonto_de_rubro(etapa_rubro, financiamiento):
    """ContratoMonto de `etapa_rubro` para `financiamiento`: usa `rubro_certificado_rubro`
    si está vinculado (rubros con más de un financiamiento a la vez), o cae al
    `rubro_contratomonto` puntual ya vinculado al rubro si corresponde al mismo
    financiamiento (caso común, un solo financiamiento).

    `CertificadoRubro` es un catálogo compartido entre TODAS las obras (ej. "Nexos y
    Redes" no es exclusivo de esta obra) — por eso la búsqueda vía `rubro_certificado_rubro`
    tiene que acotarse también al Contrato vigente de la obra dueña de `etapa_rubro`, o
    puede traer por error el ContratoMonto de una obra completamente distinta que
    comparta el mismo Rubro de Certificado + Financiamiento."""
    rubro_certificado = etapa_rubro.rubro_certificado_rubro
    if rubro_certificado is not None:
        contrato_vigente = etapa_rubro.rubro_plan.trabajos_obra.contrato_vigente()
        if contrato_vigente is None:
            return None
        return ContratoMonto.objects.filter(
            contratomonto_contrato=contrato_vigente,
            contratomonto_rubro=rubro_certificado,
            contratomonto_financiamiento=financiamiento,
        ).first()

    contratomonto = etapa_rubro.rubro_contratomonto
    if contratomonto is not None and contratomonto.contratomonto_financiamiento_id == financiamiento.pk:
        return contratomonto
    return None


class _Lote:
    def __init__(self, etapa):
        self.etapa = etapa
        self.saldo_pendiente = etapa.etapa_pct_proyectado_mes()
        self.tasa_resuelta = None
        self.tasa_fecha = None


def resolver_tasas_periodo(foja, financiamiento):
    """Resuelve, para `foja` y un financiamiento dado, los tramos (pct del rubro, tasa
    UVI->$ ya resuelta) que esa Foja liquida, aplicando el mecanismo de "lotes" FIFO de
    la Ley 27397: cada Etapa (mes proyectado) es un lote con un objetivo y un saldo
    pendiente, y cada Foja real (en orden de foja_numero) abona FIFO al lote más antiguo
    con saldo pendiente, pudiendo abonar a más de un lote en una sola Foja (recuperación
    de atraso).

    No calcula montos en pesos (eso es responsabilidad de certificado_monto_pesos_foja).
    """
    rubro = foja.foja_rubro
    chain_ids = rubro.rubro_cadena_ids()

    etapas = list(
        PlanDeTrabajosEtapa.objects.filter(etapa_rubro_id__in=chain_ids)
        .select_related("etapa_rubro")
        .order_by("etapa_fecha", "etapa_numero")
    )
    if not etapas:
        raise SinProyeccionError(rubro)
    lotes = [_Lote(etapa) for etapa in etapas]

    fojas = FojaDeMedicion.objects.filter(
        foja_rubro_id__in=chain_ids, foja_numero__lte=foja.foja_numero
    ).order_by("foja_numero")

    acumulado_real = Decimal("0")
    tasa_vigente = None
    tasa_vigente_fecha = None
    indice_lote = 0
    tramos = []

    for f in fojas:
        monto_a_repartir = f.foja_pct_avance_mes()
        es_objetivo = f.pk == foja.pk

        while monto_a_repartir > 0:
            if indice_lote >= len(lotes):
                if es_objetivo:
                    raise ProyeccionInsuficienteError(rubro, monto_a_repartir)
                break

            lote = lotes[indice_lote]
            if lote.saldo_pendiente <= 0:
                indice_lote += 1
                continue

            abono = min(monto_a_repartir, lote.saldo_pendiente)

            if lote.tasa_resuelta is not None:
                tasa, fecha = lote.tasa_resuelta, lote.tasa_fecha
            else:
                acumulado_proyectado = lote.etapa.etapa_pct_proyectado_acumulado()
                cumple_90 = (acumulado_real + abono) >= Decimal("0.90") * acumulado_proyectado
                if cumple_90:
                    fecha_tasa = lote.etapa.etapa_fecha
                    tasa = cotizacion_fin_de_mes(fecha_tasa)
                    fecha = fin_de_mes(fecha_tasa)
                    lote.tasa_resuelta, lote.tasa_fecha = tasa, fecha
                elif tasa_vigente is not None:
                    tasa, fecha = tasa_vigente, tasa_vigente_fecha
                else:
                    contratomonto = _contratomonto_de_rubro(lote.etapa.etapa_rubro, financiamiento)
                    if contratomonto is None:
                        raise SinMontoBaseUviError(lote.etapa)
                    tasa = tasa_contrato(contratomonto)
                    fecha = contratomonto.contratomonto_uvi_fecha

            tasa_vigente, tasa_vigente_fecha = tasa, fecha
            if es_objetivo:
                tramos.append(TramoResuelto(pct=abono, tasa_valor=tasa, tasa_fecha=fecha, lote=lote.etapa))

            lote.saldo_pendiente -= abono
            acumulado_real += abono
            monto_a_repartir -= abono
            if lote.saldo_pendiente == 0:
                indice_lote += 1

    return tramos


def tramos_a_pesos(tramos, financiamiento):
    """Convierte una lista de TramoResuelto (ya calculada por resolver_tasas_periodo) a
    pesos, usando el monto base en UVI del ContratoMonto de la etapa dueña de cada tramo
    (que puede diferir del ContratoMonto que se está certificando si el rubro fue
    reprogramado y el tramo pertenece a una etapa de una versión anterior con su propio
    ContratoMonto)."""
    total = Decimal("0")
    for tramo in tramos:
        contratomonto_lote = _contratomonto_de_rubro(tramo.lote.etapa_rubro, financiamiento)
        if contratomonto_lote is None or not contratomonto_lote.contratomonto_uvi:
            raise SinMontoBaseUviError(tramo.lote)
        total += (tramo.pct / Decimal("100")) * contratomonto_lote.contratomonto_uvi * tramo.tasa_valor
    return total


def certificado_monto_pesos_foja(foja, contratomonto):
    """Con lógica de atraso/lotes: resuelve los tramos de esta Foja para el
    financiamiento de `contratomonto` y los convierte a pesos (ver tramos_a_pesos)."""
    financiamiento = contratomonto.contratomonto_financiamiento
    tramos = resolver_tasas_periodo(foja, financiamiento)
    return tramos_a_pesos(tramos, financiamiento)


def certificado_monto_uvi_foja(foja, contratomonto):
    """Sin lógica de atraso: avance real del mes * monto en UVI del ContratoMonto de este
    financiamiento. None si no tiene componente UVI (no aplica Ley 27397 en absoluto,
    comportamiento naive sin cambios)."""
    if not contratomonto.contratomonto_uvi:
        return None
    return (foja.foja_pct_avance_mes() / Decimal("100")) * contratomonto.contratomonto_uvi
