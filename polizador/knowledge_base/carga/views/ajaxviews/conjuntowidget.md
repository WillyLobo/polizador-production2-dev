---
symbol: conjuntowidget
kind: class
module: carga/views/ajaxviews.py
lines: 65-69
signature_hash: sha1:b6c20af2003dbc1e28409336dbe6a73857f3f06a
authored: true
---

# conjuntowidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 65-69) · hereda de `AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) ConjuntoLicitado vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Con botón de alta rápida (`AddRelatedWidgetMixin` → `carga:crear-conjunto`).

## Firma

```python
class conjuntowidget(AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Obra.obra_conjunto` en `ObraForm`.

## Ver también

- [ConjuntoLicitado](../../models/ConjuntoLicitado.md)
- [AddRelatedWidgetMixin](AddRelatedWidgetMixin.md)
