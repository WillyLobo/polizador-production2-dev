---
symbol: categoriawidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 22-24
signature_hash: sha1:cafc6c26bf8448efd2215577c39851cc4c6b0ec4
authored: true
---

# categoriawidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 22-24) · hereda de `AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir Categoria vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Catálogo chico, con alta rápida (`personalizador:crear-categoria`).

## Firma

```python
class categoriawidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Agente.categoria` en `AgenteForm`.

## Ver también

- [Categoria](../../models/Categoria.md)
