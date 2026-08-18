---
symbol: rubroanteriorwidget
kind: class
module: carga/views/ajaxviews.py
lines: 82-97
signature_hash: sha1:3d5355daabb9804ae4403a4b61e3350f121f564a
authored: true
---

# rubroanteriorwidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 82-97) · hereda de `PlanDependentWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget para el campo "Rubro Anterior (Plan Previo)" de `PlanDeTrabajosRubroForm" — los
candidatos son rubros de la **misma Obra** pero de un Plan **distinto** al que se está
editando (`PlanDependentWidgetMixin` + `filter_queryset` propio que excluye
`rubro_plan_id=plan.pk`). Es la UI que arma la cadena de reprogramación
(`rubro_anterior`/`rubro_siguiente`) descrita en la página de
[PlanDeTrabajosRubro](../../models/PlanDeTrabajosRubro.md).

## Firma

```python
class rubroanteriorwidget(PlanDependentWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`PlanDeTrabajosRubro.rubro_anterior` en `PlanDeTrabajosRubroForm`.

## Ver también

- [PlanDeTrabajosRubro](../../models/PlanDeTrabajosRubro.md)
- [PlanDependentWidgetMixin](PlanDependentWidgetMixin.md)
