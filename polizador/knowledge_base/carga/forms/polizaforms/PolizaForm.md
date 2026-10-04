---
symbol: PolizaForm
kind: class
module: carga/forms/polizaforms.py
lines: 16-64
signature_hash: sha1:40c010a2417b466393923583ba411ec73900e052
authored: true
---

# PolizaForm

**Módulo:** `carga/forms/polizaforms.py` (líneas 16-64) · hereda de `AddRelatedPermissionMixin, forms.ModelForm`

## Propósito

`ModelForm` para Poliza, con `AddRelatedPermissionMixin` (varios de sus campos — aseguradora, tomador — usan `AddRelatedWidgetMixin` para alta rápida). Sin `clean()` propio: la validación vive en `Poliza.clean()`. Los choices de concepto se toman del modelo (`Poliza.CONCEPTO`), ya no de una copia local en el form.

Agrega los campos que alimentan el monto de garantía sugerido: `poliza_contrato` usa `contratowidget` dependiente de `poliza_obra` (sólo ofrece Contratos de esa Obra), más `poliza_financiamiento` y `poliza_anticipo_pct`. `__init__` marca `poliza_contrato` y `poliza_financiamiento` como obligatorios en el form, aunque en el modelo sean `null=True` por las pólizas legacy. Así toda póliza nueva o editada queda con base para calcular el sugerido.

## Firma

```python
class PolizaForm(AddRelatedPermissionMixin, forms.ModelForm):
```

## Uso real

`CrearPoliza`/`UpdatePoliza` (`carga/views/polizaviews.py`).

## Ver también

- [Poliza](../../models/Poliza.md)
- [AddRelatedPermissionMixin](../mixins/AddRelatedPermissionMixin.md)

- [monto_garantia_sugerido](../../../api/views/carga_views/monto_garantia_sugerido.md) — el form lo consulta en vivo.
