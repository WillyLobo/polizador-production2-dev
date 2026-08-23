---
symbol: provinciawidget
kind: class
module: carga/views/ajaxviews.py
lines: 191-194
signature_hash: sha1:26b1810eca33fab2dc5549a6a2449fd2f63da14c
authored: true
---

# provinciawidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 191-194) · hereda de `SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Provincia vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Catálogo chico (`SmallCatalogWidgetMixin`).

## Firma

```python
class provinciawidget(SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

Selección de Provincia donde se use (formularios geográficos).

## Ver también

- [Provincia](../../models/Provincia.md)
