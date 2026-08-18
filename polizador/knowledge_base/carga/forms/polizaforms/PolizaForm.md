---
symbol: PolizaForm
kind: class
module: carga/forms/polizaforms.py
lines: 16-54
signature_hash: sha1:afbf455819c14fb012bcf5d434d752801aab2e47
authored: true
---

# PolizaForm

**Módulo:** `carga/forms/polizaforms.py` (líneas 16-54) · hereda de `AddRelatedPermissionMixin, forms.ModelForm`

## Propósito

`ModelForm` para Poliza, con `AddRelatedPermissionMixin` (varios de sus campos — aseguradora, tomador — usan `AddRelatedWidgetMixin` para alta rápida). Sin `clean()` propio.

## Firma

```python
class PolizaForm(AddRelatedPermissionMixin, forms.ModelForm):
```

## Uso real

`CrearPoliza`/`UpdatePoliza` (`carga/views/polizaviews.py`).

## Ver también

- [Poliza](../../models/Poliza.md)
- [AddRelatedPermissionMixin](AddRelatedPermissionMixin.md)
