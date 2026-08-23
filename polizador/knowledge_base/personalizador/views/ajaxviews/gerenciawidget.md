---
symbol: gerenciawidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 50-52
signature_hash: sha1:6165a3ac61ca276ed9ebc438e960a156f2771bf2
authored: true
---

# gerenciawidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 50-52) · hereda de `AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir Gerencia vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Catálogo chico, con alta rápida (`personalizador:crear-gerencia`).

## Firma

```python
class gerenciawidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Direccion.direccion_gerencia`, `Departamento.departamento_gerencia` en sus forms.

## Ver también

- [Gerencia](../../models/Gerencia.md)
