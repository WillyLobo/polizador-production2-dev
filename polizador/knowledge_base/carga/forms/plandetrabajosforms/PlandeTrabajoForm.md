---
symbol: PlandeTrabajoForm
kind: class
module: carga/forms/plandetrabajosforms.py
lines: 6-26
signature_hash: sha1:a5af2440a8595a609280ead2b333fe90c5fa97de
authored: true
---

# PlandeTrabajoForm

**Módulo:** `carga/forms/plandetrabajosforms.py` (líneas 6-26) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para `PlanDeTrabajos` (Obra, fecha de vigencia, duración en meses, Contrato vinculado opcional). El campo `trabajos_contrato` usa `contratowidget` con `dependent_fields` sobre `trabajos_obra` — solo ofrece Contratos de la Obra elegida, seteado a mano en el widget (no vía un mixin, a diferencia de `PlanDependentWidgetMixin`).

## Firma

```python
class PlandeTrabajoForm(forms.ModelForm):
```

## Uso real

`CrearPlanDeTrabajos`/`UpdatePlanDeTrabajos` (`carga/views/plandetrabajosviews.py`).

## Ver también

- [PlanDeTrabajos](../../models/PlanDeTrabajos.md)
- [contratowidget](../../views/ajaxviews/contratowidget.md)
