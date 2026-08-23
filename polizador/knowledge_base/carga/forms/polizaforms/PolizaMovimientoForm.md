---
symbol: PolizaMovimientoForm
kind: class
module: carga/forms/polizaforms.py
lines: 56-73
signature_hash: sha1:91cad77e416e4d3261d8c34b71690efba1b1cb33
authored: true
---

# PolizaMovimientoForm

**Módulo:** `carga/forms/polizaforms.py` (líneas 56-73) · hereda de `AddRelatedPermissionMixin, forms.ModelForm`

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
