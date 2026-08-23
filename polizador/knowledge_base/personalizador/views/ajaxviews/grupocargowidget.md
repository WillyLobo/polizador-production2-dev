---
symbol: grupocargowidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 38-40
signature_hash: sha1:e9c0045c7a35204ca8382ba1f5f8ef4ddfa88b58
authored: true
---

# grupocargowidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 38-40) · hereda de `AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir GrupoCargo vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Catálogo chico, con alta rápida (`personalizador:crear-grupocargo`).

## Firma

```python
class grupocargowidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Agente.grupo` en `AgenteForm`.

## Ver también

- [GrupoCargo](../../models/GrupoCargo.md)
