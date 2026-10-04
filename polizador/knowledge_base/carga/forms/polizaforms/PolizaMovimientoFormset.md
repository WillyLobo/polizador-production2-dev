---
symbol: PolizaMovimientoFormset
kind: class
module: carga/forms/polizaforms.py
lines: 85-87
signature_hash: sha1:38c528a27ee8b67f278b2532bbbe90d581296d0f
authored: true
---

# PolizaMovimientoFormset

**Módulo:** `carga/forms/polizaforms.py` (líneas 85-87) · hereda de `forms.models.BaseInlineFormSet`

## Propósito

Formset inline de `Poliza_Movimiento` sobre una Poliza (`can_delete=False`). Mismo `__init__` vestigial que `ContratoMontoFormset` (no agrega nada sobre la clase base).

## Firma

```python
class PolizaMovimientoFormset(forms.models.BaseInlineFormSet):
```

## Uso real

`formset_name = PolizaMovimientoFormset` en `CrearPoliza`/`UpdatePoliza`.

## Ver también

- [Poliza_Movimiento](../../models/Poliza_Movimiento.md)
- [PolizaMovimientoForm](PolizaMovimientoForm.md)
