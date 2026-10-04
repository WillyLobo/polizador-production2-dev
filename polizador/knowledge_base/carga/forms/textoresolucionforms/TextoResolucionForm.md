---
symbol: TextoResolucionForm
kind: class
module: carga/forms/textoresolucionforms.py
lines: 23-39
signature_hash: sha1:649b59531bbaf1f8f709bba41d9e377bc91f16ac
authored: true
---

# TextoResolucionForm

**Módulo:** `carga/forms/textoresolucionforms.py` (líneas 23-39) · hereda de `forms.ModelForm`

## Propósito

Form del **alcance** de una plantilla: nombre, programa (`programawidget`),
financiamiento y tipo de certificado (vacío = comodín). Los bloques no pasan por acá: van en
`BloqueFormSet` y la vista los asigna a `textoresolucion_bloques` antes de guardar. La
unicidad del alcance la valida la `UniqueConstraint` del modelo.

## Firma

```python
class TextoResolucionForm(forms.ModelForm):
```

## Uso real

`form_class` de [TextoResolucionEditorMixin](../../views/textoresolucionviews/TextoResolucionEditorMixin.md).

## Ver también

- [TextoResolucionCertificado](../../models/TextoResolucionCertificado.md)
- [BloqueForm](BloqueForm.md)
