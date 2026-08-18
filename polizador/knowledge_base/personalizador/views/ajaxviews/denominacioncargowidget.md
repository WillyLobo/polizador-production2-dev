---
symbol: denominacioncargowidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 26-28
signature_hash: sha1:e1f509c86207f2b066a7b2c3016c106b20eb4b2f
authored: true
---

# denominacioncargowidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 26-28) · hereda de `AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir DenominacionCargo vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Catálogo chico, con alta rápida (`personalizador:crear-denominacioncargo`).

## Firma

```python
class denominacioncargowidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Agente.denominacion_cargo` en `AgenteForm`.

## Ver también

- [DenominacionCargo](../../models/DenominacionCargo.md)
