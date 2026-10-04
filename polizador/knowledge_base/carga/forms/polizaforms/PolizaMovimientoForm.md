---
symbol: PolizaMovimientoForm
kind: class
module: carga/forms/polizaforms.py
lines: 66-83
signature_hash: sha1:83359e124a55dc7eb288b1b612407fbc7581523a
authored: true
---

# PolizaMovimientoForm

**Módulo:** `carga/forms/polizaforms.py` (líneas 66-83) · hereda de `AddRelatedPermissionMixin, forms.ModelForm`

## Propósito

`ModelForm` para `Poliza_Movimiento` (fecha, receptor, área, número de póliza), con `AddRelatedPermissionMixin`.

## Firma

```python
class PolizaMovimientoForm(AddRelatedPermissionMixin, forms.ModelForm):
```

## Uso real

Form base de `PolizaMovimientoFormset`.

## Ver también

- [Poliza_Movimiento](../../models/Poliza_Movimiento.md)
