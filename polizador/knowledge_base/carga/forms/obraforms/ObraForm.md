---
symbol: ObraForm
kind: class
module: carga/forms/obraforms.py
lines: 20-170
signature_hash: sha1:2e582a44a334b21e3cb5f3dbd2273315d207f2c6
authored: true
---

# ObraForm

**Módulo:** `carga/forms/obraforms.py` (líneas 20-170) · hereda de `AddRelatedPermissionMixin, forms.ModelForm`

## Propósito

El `ModelForm` más grande de `carga`: ~30 campos de Obra, todos declarados vía
`Meta.fields`/`widgets` sin ningún `clean()` propio — la validación real de negocio de
Obra vive en `Obra.clean()` (a nivel modelo), no acá. La única pieza no estándar es el
campo `obra_georeferencia`: no usa el `PointField` de GIS directamente, sino un
`LatLngField`/`LatLngWidget` (`core.widgets`) a medida — probablemente porque el widget
nativo de `django.contrib.gis` para un `PointField` no encaja con el resto del layout
Bootstrap del sitio, y este par convierte lat/lng planos a `Point` en la limpieza del
form.

## Firma

```python
class ObraForm(AddRelatedPermissionMixin, forms.ModelForm):
```

## Uso real

`CrearObra`/`UpdateObra` (`carga/views/obraviews.py`).

## Ver también

- [Obra](../../models/Obra.md)
- [AddRelatedPermissionMixin](AddRelatedPermissionMixin.md)
