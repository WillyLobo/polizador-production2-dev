---
symbol: programawidget
kind: class
module: carga/views/ajaxviews.py
lines: 99-103
signature_hash: sha1:b0d21eabac6d9e56a2f79832452d11feb997be31
authored: true
---

# programawidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 99-103) · hereda de `AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Programa vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Catálogo chico (`SmallCatalogWidgetMixin`) con alta rápida (`AddRelatedWidgetMixin` → `carga:crear-programa`).

## Firma

```python
class programawidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Obra.obra_programa` en `ObraForm`.

## Ver también

- [Programa](../../models/Programa.md)
