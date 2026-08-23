---
symbol: ceicwidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 34-36
signature_hash: sha1:47cbb36413d3fb4007ebaf24f3b379739c21f3ec
authored: true
---

# ceicwidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 34-36) · hereda de `AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir CEIC vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Catálogo chico, con alta rápida (`personalizador:crear-ceic`).

## Firma

```python
class ceicwidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Agente.ceic` en `AgenteForm`.

## Ver también

- [CEIC](../../models/CEIC.md)
