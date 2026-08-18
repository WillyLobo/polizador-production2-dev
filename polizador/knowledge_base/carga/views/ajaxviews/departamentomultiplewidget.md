---
symbol: departamentomultiplewidget
kind: class
module: carga/views/ajaxviews.py
lines: 196-199
signature_hash: sha1:9ea6f0ee7b8fa397cd0bf402300dd7a09a51d1d2
authored: true
---

# departamentomultiplewidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 196-199) · hereda de `SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Departamento vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Selección múltiple, catálogo chico.

## Firma

```python
class departamentomultiplewidget(SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
```

## Uso real

Campos `ManyToManyField` a Departamento.

## Ver también

- [Departamento](../../models/Departamento.md)
