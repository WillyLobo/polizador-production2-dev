"""
Armado del contexto de un Certificado: los datos resueltos (financiamiento,
contrato, montos por rubro, incidencias, tramos Ley 27397, cotizacion UVI
usada, resumen de certificacion y firmantes institucionales) que describen a
un certificado ya guardado.

Vivia dentro de `carga/views/certificadoviews.py`, pero ese modulo hace
`from carga.forms.certificadoforms import *`, con lo cual importarlo desde un
codepath de generacion de documentos arrastraria forms, widgets y Select2, con
riesgo de ciclo de import. Aca no hay ninguna dependencia de vistas ni de forms:
son funciones puras sobre modelos.

Consumidores: `carga/views/certificadoviews.py` (ficha e impresion del
certificado) y `carga/resolucion_texto.py` (texto de la resolucion).
"""
from datetime import date
from decimal import Decimal

from carga.certificacion import resumen_certificacion_mensual
from carga.ley27397 import _contratomonto_de_rubro
from carga.models import CertificadoFinanciamiento, ContratoMonto, FojaDeMedicion, PlanDeTrabajosEtapa, Uvi
from personalizador.models import Departamento, Direccion, Directorio, Gerencia

def _desglose_items_certificado(certificado, contratomonto_rubro):
    """Costo por ítem de la Foja de origen de `certificado`: cada fila es un
    FojaDeMedicionItem con su % de incidencia dentro del rubro (fijo, del plan de
    trabajos) y su avance anterior/mes/acumulado, valorizado contra el
    ContratoMonto del rubro+financiamiento de este certificado. Sin Foja de origen
    (Anticipo, Hecho Consumado, legacy) no hay ítems que desglosar."""
    if not certificado.certificado_foja_id or certificado.certificado_tipo == "ETAPA":
        # ETAPA sí tiene Foja (es la que disparó el tramo), pero su monto sale del % fijo
        # del tramo, no del avance real del mes: mostrar el desglose por ítem sería
        # engañoso (no es la base de lo que efectivamente se certificó).
        return None

    foja = certificado.certificado_foja
    rubro = foja.foja_rubro
    items = list(foja.items.select_related("fojaitem_planitem").order_by("fojaitem_planitem__planitem_orden"))
    anterior_map = FojaDeMedicion.anterior_items_map(rubro, exclude_foja_numero=foja.foja_numero)

    base_uvi = contratomonto_rubro.contratomonto_uvi if contratomonto_rubro else Decimal("0")
    base_pesos = contratomonto_rubro.contratomonto_pesos if contratomonto_rubro else Decimal("0")

    filas = []
    for item in items:
        planitem = item.fojaitem_planitem
        incidencia_pct = planitem.planitem_incidencia_pct
        pct_anterior = anterior_map.get(planitem.pk, Decimal("0"))
        pct_mes = item.fojaitem_pct_avance_mes
        pct_acumulado = item.fojaitem_pct_acumulado

        if base_uvi:
            monto_basico_uvi = incidencia_pct / Decimal("100") * base_uvi
            monto_total_uvi = pct_acumulado / Decimal("100") * base_uvi
            monto_basico_pesos = Uvi.pesos_equivalentes(monto_basico_uvi, certificado.certificado_fecha)
            monto_total_pesos = Uvi.pesos_equivalentes(monto_total_uvi, certificado.certificado_fecha)
        else:
            monto_basico_uvi = None
            monto_total_uvi = None
            monto_basico_pesos = incidencia_pct / Decimal("100") * base_pesos
            monto_total_pesos = pct_acumulado / Decimal("100") * base_pesos

        filas.append({
            "nombre": planitem.planitem_nombre,
            "incidencia_pct": incidencia_pct,
            "pct_anterior": pct_anterior,
            "pct_mes": pct_mes,
            "pct_acumulado": pct_acumulado,
            "monto_basico_uvi": monto_basico_uvi,
            "monto_basico_pesos": monto_basico_pesos,
            "monto_total_uvi": monto_total_uvi,
            "monto_total_pesos": monto_total_pesos,
        })
    return filas


def _certificado_detalle_context(certificado):
    obra = certificado.certificado_obra
    financiamiento = CertificadoFinanciamiento.objects.filter(
        certificadofinanciamiento_nombre_corto=certificado.certificado_financiamiento
    ).first()
    # Un Hecho Consumado certifica contra su propio Contrato/Resolución de origen (elegido a
    # mano, no necesariamente el vigente de la obra); PARCIAL/ANTICIPO sí usan el vigente.
    contrato_certificado = certificado.certificado_contrato_origen or obra.contrato_vigente()
    contratomontos = (
        ContratoMonto.objects.filter(contratomonto_contrato=contrato_certificado).select_related(
            "contratomonto_rubro", "contratomonto_financiamiento"
        )
        if contrato_certificado
        else ContratoMonto.objects.none()
    )
    contratomonto_rubro = contratomontos.filter(
        contratomonto_rubro=certificado.certificado_rubro_db, contratomonto_financiamiento=financiamiento
    ).first()
    mismo_financiamiento = [cm for cm in contratomontos if financiamiento and cm.contratomonto_financiamiento_id == financiamiento.pk]
    total_pesos_financiamiento = sum((cm.contratomonto_pesos for cm in mismo_financiamiento), Decimal("0"))
    total_uvi_financiamiento = sum((cm.contratomonto_uvi for cm in mismo_financiamiento), Decimal("0"))
    incidencia_pct_pesos = (
        contratomonto_rubro.contratomonto_pesos / total_pesos_financiamiento * 100
        if contratomonto_rubro and total_pesos_financiamiento
        else None
    )
    incidencia_pct_uvi = (
        contratomonto_rubro.contratomonto_uvi / total_uvi_financiamiento * 100
        if contratomonto_rubro and total_uvi_financiamiento
        else None
    )
    plan = certificado.certificado_foja.foja_rubro.rubro_plan if certificado.certificado_foja_id else obra.plan_vigente()

    # Monto en UVI/pesos de cada tramo, misma cuenta que carga.ley27397.tramos_a_pesos: el
    # ContratoMonto puede ser el de una versión anterior del rubro (reprogramación), no
    # necesariamente el vigente que se resolvió arriba para `contratomonto_rubro`.
    tramos_ley27397 = []
    for tramo in (certificado.certificado_ley27397_detalle or []):
        etapa = PlanDeTrabajosEtapa.objects.filter(pk=tramo["etapa_id"]).select_related("etapa_rubro").first()
        contratomonto_lote = _contratomonto_de_rubro(etapa.etapa_rubro, financiamiento) if etapa and financiamiento else None
        if contratomonto_lote:
            monto_uvi_tramo = Decimal(tramo["pct"]) / Decimal("100") * contratomonto_lote.contratomonto_uvi
            monto_pesos_tramo = monto_uvi_tramo * Decimal(tramo["tasa_valor"])
        else:
            monto_uvi_tramo = monto_pesos_tramo = None
        tramos_ley27397.append({
            **tramo,
            "tasa_fecha": date.fromisoformat(tramo["tasa_fecha"]),
            "monto_uvi": monto_uvi_tramo,
            "monto_pesos": monto_pesos_tramo,
        })

    ultimo_tramo = (certificado.certificado_ley27397_detalle or [None])[-1]

    # Cotización UVI efectivamente usada para pasar este certificado a pesos: el último
    # tramo de Ley 27397 si tiene Foja (PARCIAL), o la de certificado_fecha si no (Anticipo,
    # Hecho Consumado — ver calcular_monto_anticipo/calcular_monto_hecho_consumado).
    if ultimo_tramo:
        uvi_fecha_calculo = date.fromisoformat(ultimo_tramo["tasa_fecha"])
        uvi_valor_calculo = ultimo_tramo["tasa_valor"]
    elif certificado.certificado_monto_uvi:
        uvi_calculo = Uvi.objects.filter(uvi_fecha__lte=certificado.certificado_fecha).order_by("-uvi_fecha").first()
        uvi_fecha_calculo = uvi_calculo.uvi_fecha if uvi_calculo else None
        uvi_valor_calculo = uvi_calculo.uvi_valor if uvi_calculo else None
    else:
        uvi_fecha_calculo = uvi_valor_calculo = None

    presidente = Directorio.objects.filter(directorio_nombre="Presidencia").first()
    gerencia_operativa = Gerencia.objects.filter(gerencia_nombre="Gerencia Operativa").first()
    direccion_certificaciones = Direccion.objects.filter(direccion_nombre="Certificaciones").first()
    departamento_certificaciones = Departamento.objects.filter(departamento_nombre="Certificados De Obras").first()

    gerente_agente = gerencia_operativa.gerencia_autoridad_a_cargo_fk if gerencia_operativa else None
    directora_agente = direccion_certificaciones.direccion_autoridad_a_cargo_fk if direccion_certificaciones else None
    jefe_agente = departamento_certificaciones.departamento_autoridad_a_cargo_fk if departamento_certificaciones else None

    return {
        "obra": obra,
        "financiamiento": financiamiento,
        "plan": plan,
        "contratomontos": contratomontos,
        "contratomonto_rubro": contratomonto_rubro,
        "incidencia_pct_pesos": incidencia_pct_pesos,
        "incidencia_pct_uvi": incidencia_pct_uvi,
        "tramo": certificado.certificado_contrato_tramo,
        "desglose_items": _desglose_items_certificado(certificado, contratomonto_rubro),
        "tramos_ley27397": tramos_ley27397,
        "ultimo_tramo": ultimo_tramo,
        "uvi_fecha_calculo": uvi_fecha_calculo,
        "uvi_valor_calculo": uvi_valor_calculo,
        "resumen": resumen_certificacion_mensual(certificado),
        "presidente": presidente,
        "hoja1_firmantes": [{"agente": gerente_agente, "cargo": "GERENTE OPERATIVO"}],
        "hoja2_firmantes": [
            {"agente": directora_agente, "cargo": "DIRECTORA DE CERTIFICACIONES"},
            {"agente": gerente_agente, "cargo": "GERENTE OPERATIVO"},
        ],
        "hoja3_firmantes": [{"agente": jefe_agente, "cargo": "JEFE DPTO CERTIFICACIONES"}],
    }
