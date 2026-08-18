---
symbol: municipiomultiplewidget
kind: class
module: carga/views/ajaxviews.py
lines: 216-219
signature_hash: sha1:acdfb0b8d54359043c7e0199b99556dc2c4d4c77
authored: true
---

# municipiomultiplewidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 216-219) · hereda de `SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Municipio vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Selección múltiple, catálogo chico.

## Firma

```python
class municipiomultiplewidget(SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
```

## Uso real

`Obra.obra_municipio_m` en `ObraForm`.

## Ver también

- [Municipio](../../models/Municipio.md)
