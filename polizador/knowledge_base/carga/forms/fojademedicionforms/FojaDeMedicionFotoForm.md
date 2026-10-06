---
symbol: FojaDeMedicionFotoForm
kind: class
module: carga/forms/fojademedicionforms.py
lines: 242-250
signature_hash: sha1:85fa0ff54ed21ded072af05acc7232b14abbeb61
authored: true
---

# FojaDeMedicionFotoForm

**Módulo:** `carga/forms/fojademedicionforms.py` (líneas 242-250) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` mínimo para `FojaDeMedicionFoto`: un solo campo, el archivo de imagen.

## Firma

```python
class FojaDeMedicionFotoForm(forms.ModelForm):
```

## Uso real

Form base de `FojaDeMedicionFotoFormset`, usado en `CrearFojaDeMedicion`/`UpdateFojaDeMedicion`.

## Ver también

- [FojaDeMedicionFoto](../../models/FojaDeMedicionFoto.md)
