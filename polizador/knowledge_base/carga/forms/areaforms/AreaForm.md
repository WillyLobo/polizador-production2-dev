---
symbol: AreaForm
kind: class
module: carga/forms/areaforms.py
lines: 4-14
signature_hash: sha1:b89eef700fcca3dbd7dfc7a62895c23086472db9
authored: true
---

# AreaForm

**Módulo:** `carga/forms/areaforms.py` (líneas 4-14) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para Area, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets` (inputs Bootstrap, sin validación más allá de la del modelo). Un solo campo: `area_nombre`.

## Firma

```python
class AreaForm(forms.ModelForm):
```

## Uso real

`CrearArea/UpdateArea` (`carga/views/`), tanto para alta como edición.

## Ver también

- [Area](../../models/Area.md)
