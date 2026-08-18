---
symbol: PlanDeTrabajosItemFormset
kind: class
module: carga/forms/plandetrabajosrubroforms.py
lines: 56-69
signature_hash: sha1:631f8693cb50b362f0174e67a28f47773b014509
authored: true
---

# PlanDeTrabajosItemFormset

**Módulo:** `carga/forms/plandetrabajosrubroforms.py` (líneas 56-69) · hereda de `forms.models.BaseInlineFormSet`

## Propósito

Formset inline de `PlanDeTrabajosItem` sobre un Rubro, con la misma validación de conjunto que `ContratoTramoPagoFormset`: la suma de `planitem_incidencia_pct` de todos los items (no borrados) debe dar 100% (tolerancia 0.5) — la incidencia de los items de un rubro siempre tiene que cubrir el 100% del rubro.

## Firma

```python
class PlanDeTrabajosItemFormset(forms.models.BaseInlineFormSet):
```

## Uso real

`formset_name = PlanDeTrabajosItemFormset` en `CrearPlanDeTrabajosRubro`/`UpdatePlanDeTrabajosRubro`.

## Ver también

- [PlanDeTrabajosItem](../../models/PlanDeTrabajosItem.md)
- [PlanDeTrabajosItemForm](PlanDeTrabajosItemForm.md)
