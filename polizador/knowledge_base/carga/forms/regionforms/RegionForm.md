---
symbol: RegionForm
kind: class
module: carga/forms/regionforms.py
lines: 4-14
signature_hash: sha1:28d5a0bc4d7349f2807a3224c8a2f3fa41a8b78b
authored: true
---

# RegionForm

**Módulo:** `carga/forms/regionforms.py` (líneas 4-14) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para Region, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets` (inputs Bootstrap, sin validación más allá de la del modelo). Un solo campo: `region_numero`.

## Firma

```python
class RegionForm(forms.ModelForm):
```

## Uso real

`CrearRegion/UpdateRegion` (`carga/views/`), tanto para alta como edición.

## Ver también

- [Region](../../models/Region.md)
