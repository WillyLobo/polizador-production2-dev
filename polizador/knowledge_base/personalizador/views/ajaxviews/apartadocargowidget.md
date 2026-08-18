---
symbol: apartadocargowidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 30-32
signature_hash: sha1:ea99a41e2716cb5fab6660d6d456b646d17a680c
authored: true
---

# apartadocargowidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 30-32) · hereda de `AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir ApartadoCargo vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Catálogo chico, con alta rápida (`personalizador:crear-apartadocargo`).

## Firma

```python
class apartadocargowidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Agente.apartado` en `AgenteForm`.

## Ver también

- [ApartadoCargo](../../models/ApartadoCargo.md)
