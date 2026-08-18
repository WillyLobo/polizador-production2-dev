---
symbol: departamentowidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 58-60
signature_hash: sha1:72fabbbb42f78a51171f2d55bf8491c196333fdb
authored: true
---

# departamentowidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 58-60) · hereda de `AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir Departamento (personalizador) vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Catálogo chico, con alta rápida (`personalizador:crear-departamento`). No confundir con `carga.views.ajaxviews.departamentowidget` (geográfico, modelo distinto).

## Firma

```python
class departamentowidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

Campos que referencian `personalizador.Departamento`.

## Ver también

- [Departamento](../../models/Departamento.md)
