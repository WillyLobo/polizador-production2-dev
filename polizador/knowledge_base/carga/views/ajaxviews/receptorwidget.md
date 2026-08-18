---
symbol: receptorwidget
kind: class
module: carga/views/ajaxviews.py
lines: 163-167
signature_hash: sha1:435551f7b4a6332d6ced1c5d8ca08e803ddff45c
authored: true
---

# receptorwidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 163-167) · hereda de `AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Receptor vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Con alta rápida (`carga:crear-receptor`).

## Firma

```python
class receptorwidget(AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Poliza_Movimiento.poliza_movimiento_receptor` en `PolizaMovimientoForm`.

## Ver también

- [Receptor](../../models/Receptor.md)
