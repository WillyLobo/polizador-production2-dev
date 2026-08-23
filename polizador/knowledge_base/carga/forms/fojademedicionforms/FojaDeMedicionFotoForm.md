---
symbol: FojaDeMedicionFotoForm
kind: class
module: carga/forms/fojademedicionforms.py
lines: 230-238
signature_hash: sha1:366657168ba190067eb43f03c023df5ea7f34f29
authored: true
---

# FojaDeMedicionFotoForm

**Módulo:** `carga/forms/fojademedicionforms.py` (líneas 230-238) · hereda de `forms.ModelForm`

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
