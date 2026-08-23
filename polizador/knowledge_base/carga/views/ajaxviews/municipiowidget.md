---
symbol: municipiowidget
kind: class
module: carga/views/ajaxviews.py
lines: 221-224
signature_hash: sha1:e5fdebbd5ecca1c7d70e4e513df3fa76dd9e6fb5
authored: true
---

# municipiowidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 221-224) · hereda de `SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Municipio vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Catálogo chico, selección simple.

## Firma

```python
class municipiowidget(SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

Campos `ForeignKey` a Municipio (ej. `Localidad.localidad_municipio`).

## Ver también

- [municipiomultiplewidget](municipiomultiplewidget.md)
