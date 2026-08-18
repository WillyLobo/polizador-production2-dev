---
symbol: PolizaMovimientoFormset
kind: class
module: carga/forms/polizaforms.py
lines: 75-77
signature_hash: sha1:530425ae99c5f3bf395762e3e642558e22c219ae
authored: true
---

# PolizaMovimientoFormset

**Módulo:** `carga/forms/polizaforms.py` (líneas 75-77) · hereda de `forms.models.BaseInlineFormSet`

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
