---
symbol: areawidget
kind: class
module: carga/views/ajaxviews.py
lines: 157-161
signature_hash: sha1:9a5bf7772dea4232a802c56f4ba65420df7ff4c4
authored: true
---

# areawidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 157-161) · hereda de `AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Area vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Catálogo chico, con alta rápida (`carga:crear-area`).

## Firma

```python
class areawidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Poliza_Movimiento.poliza_movimiento_area` en `PolizaMovimientoForm`.

## Ver también

- [Area](../../models/Area.md)
