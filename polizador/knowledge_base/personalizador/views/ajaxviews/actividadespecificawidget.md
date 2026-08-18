---
symbol: actividadespecificawidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 42-44
signature_hash: sha1:07e2e05a0c27f85669da67bdabe6987a83be17a5
authored: true
---

# actividadespecificawidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 42-44) · hereda de `AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir ActividadEspecifica vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Catálogo chico, con alta rápida (`personalizador:crear-actividadespecifica`).

## Firma

```python
class actividadespecificawidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Agente.actividad_especifica` en `AgenteForm`.

## Ver también

- [ActividadEspecifica](../../models/ActividadEspecifica.md)
