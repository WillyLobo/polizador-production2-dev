from carga.models import (
    Contrato, ContratoMonto, ContratosDigitales, ContratoTramoPago,
    FojaDeMedicion, FojaDeMedicionFoto, FojaDeMedicionItem,
    Obra, ObraDocumento, Poliza, Poliza_Movimiento, PolizaDocumento, Prototipo,
    PlanDeTrabajos, PlanDeTrabajosEtapa, PlanDeTrabajosEtapaItem, PlanDeTrabajosItem, PlanDeTrabajosRubro,
)
from core.history import HistorySource, build_timeline, register


def _ultimo_por_id(rows, attr):
    # Filas ordenadas por fecha: queda el último valor conocido, aun si el objeto ya fue eliminado.
    return {r.id: getattr(r, attr) for r in sorted(rows, key=lambda r: r.history_date)}


def plandetrabajos_sources(plan):
    planes = list(PlanDeTrabajos.trabajos_history.filter(id=plan.pk).select_related("history_user"))
    rubros = list(PlanDeTrabajosRubro.rubro_history.filter(rubro_plan_id=plan.pk).select_related("history_user"))
    rubro_ids = {r.id for r in rubros}
    items = list(PlanDeTrabajosItem.planitem_history.filter(planitem_rubro_id__in=rubro_ids).select_related("history_user"))
    etapas = list(PlanDeTrabajosEtapa.etapa_history.filter(etapa_rubro_id__in=rubro_ids).select_related("history_user"))
    etapaitems = list(PlanDeTrabajosEtapaItem.etapaitem_history.filter(etapaitem_etapa_id__in={e.id for e in etapas}).select_related("history_user"))
    fojas = list(FojaDeMedicion.foja_history.filter(foja_rubro_id__in=rubro_ids).select_related("history_user"))
    fojaitems = list(FojaDeMedicionItem.fojaitem_history.filter(fojaitem_foja_id__in={f.id for f in fojas}).select_related("history_user"))

    rubro_nombre = _ultimo_por_id(rubros, "rubro_nombre")
    item_nombre = _ultimo_por_id(items, "planitem_nombre")
    etapa_numero = _ultimo_por_id(etapas, "etapa_numero")
    foja_numero = _ultimo_por_id(fojas, "foja_numero")

    return [
        HistorySource("Plan", planes, lambda r: f"Plan de Trabajos (vigencia {r.trabajos_fecha:%d/%m/%Y})"),
        HistorySource("Rubros", rubros, lambda r: r.rubro_nombre),
        HistorySource("Items", items, lambda r: f"{r.planitem_nombre} · {rubro_nombre.get(r.planitem_rubro_id, '?')}"),
        HistorySource("Etapas", etapas, lambda r: f"Etapa {r.etapa_numero} · {rubro_nombre.get(r.etapa_rubro_id, '?')}"),
        HistorySource("Items de Etapa", etapaitems, lambda r: f"Etapa {etapa_numero.get(r.etapaitem_etapa_id, '?')} · {item_nombre.get(r.etapaitem_planitem_id, '?')}"),
        HistorySource("Fojas", fojas, lambda r: f"Foja {r.foja_numero} · {rubro_nombre.get(r.foja_rubro_id, '?')}"),
        HistorySource("Items de Foja", fojaitems, lambda r: f"Foja {foja_numero.get(r.fojaitem_foja_id, '?')} · {item_nombre.get(r.fojaitem_planitem_id, '?')}"),
    ]


register(PlanDeTrabajos, sources=plandetrabajos_sources)
# Obra: sin Pólizas, Certificados ni Planes, que tienen su propia página e historial.
register(Obra, children=[Contrato, ObraDocumento, Prototipo])
register(Poliza, children=[Poliza_Movimiento, PolizaDocumento])
register(Contrato, children=[ContratoTramoPago, ContratoMonto, ContratosDigitales])
register(PlanDeTrabajosRubro, children=[PlanDeTrabajosItem])
register(FojaDeMedicion, children=[FojaDeMedicionItem, FojaDeMedicionFoto])
