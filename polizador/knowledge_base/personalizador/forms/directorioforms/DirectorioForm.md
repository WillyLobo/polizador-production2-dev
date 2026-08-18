---
symbol: DirectorioForm
kind: class
module: personalizador/forms/directorioforms.py
lines: 5-23
signature_hash: sha1:3ebed6336d0bd7d07c1a3d0b685651ef3ad30bbd
authored: true
---

# DirectorioForm

**Módulo:** `personalizador/forms/directorioforms.py` (líneas 5-23) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para Directorio (nivel más alto del árbol organizacional): nombre, autoridad a cargo (texto + `agentewidget`), CUOF/UNGI. Sin lógica propia.

## Firma

```python
class DirectorioForm(forms.ModelForm):
```

## Uso real

`CrearDirectorio`/`UpdateDirectorio`.

## Ver también

- [Directorio](../../models/Directorio.md)
- [agentewidget](../ajaxviews/agentewidget.md)
