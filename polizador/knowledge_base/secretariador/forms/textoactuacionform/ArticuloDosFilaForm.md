---
symbol: ArticuloDosFilaForm
kind: class
module: secretariador/forms/textoactuacionform.py
lines: 16-20
signature_hash: sha1:207c52ea4aca3723a957a32de27c63ff4cfb2cda
authored: true
---

# ArticuloDosFilaForm

**Módulo:** `secretariador/forms/textoactuacionform.py` (líneas 16-20) · hereda de `forms.Form`

## Propósito

Una fila del Artículo 2º (el detalle de montos por comisionado): `comisionado_id` oculto (para reconciliar con `_articulo_dos_inicial` qué fila corresponde a qué comisionado real) + nombre/CUIL, monto y detalle en texto libre — todos editables a mano, no recalculados desde el modelo en este form.

## Firma

```python
class ArticuloDosFilaForm(forms.Form):
```

## Uso real

`ArticuloDosFormSet = forms.formset_factory(ArticuloDosFilaForm, extra=0)` (mismo módulo), usado en `revisar_texto_actuacion`.

## Ver también

- [_articulo_dos_inicial](../../views/textoactuacionviews/_articulo_dos_inicial.md)
