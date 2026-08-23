---
symbol: direccionwidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 54-56
signature_hash: sha1:8c176ae72d60433093773c5b8b488f9483ee623b
authored: true
---

# direccionwidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 54-56) · hereda de `AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir Direccion vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Catálogo chico, con alta rápida (`personalizador:crear-direccion`).

## Firma

```python
class direccionwidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Departamento.departamento_direccion` en `DepartamentoForm`.

## Ver también

- [Direccion](../../models/Direccion.md)
