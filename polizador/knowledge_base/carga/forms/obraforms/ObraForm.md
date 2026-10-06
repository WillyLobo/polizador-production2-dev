---
symbol: ObraForm
kind: class
module: carga/forms/obraforms.py
lines: 20-175
signature_hash: sha1:ed35e74751190a625bcbca5baa9eedaad3634e2c
authored: true
---

# ObraForm

**Módulo:** `carga/forms/obraforms.py` (líneas 20-175) · hereda de `AddRelatedPermissionMixin, forms.ModelForm`

## Propósito

El `ModelForm` más grande de `carga`: ~30 campos de Obra, todos declarados vía
`Meta.fields`/`widgets` sin ningún `clean()` propio — la validación real de negocio de
Obra vive en `Obra.clean()` (a nivel modelo), no acá. La única pieza no estándar es el
campo `obra_georeferencia`: no usa el `PointField` de GIS directamente, sino un
`LatLngField`/`LatLngWidget` (`core.widgets`) a medida — probablemente porque el widget
nativo de `django.contrib.gis` para un `PointField` no encaja con el resto del layout
Bootstrap del sitio, y este par convierte lat/lng planos a `Point` en la limpieza del
form.

Incluye `obra_fecha_inicio` (Acta de Inicio, con `DateHTMLWidget`).

## Firma

```python
class ObraForm(AddRelatedPermissionMixin, forms.ModelForm):
```

## Uso real

`CrearObra`/`UpdateObra` (`carga/views/obraviews.py`).

## Ver también

- [Obra](../../models/Obra.md)
- [AddRelatedPermissionMixin](../mixins/AddRelatedPermissionMixin.md)
