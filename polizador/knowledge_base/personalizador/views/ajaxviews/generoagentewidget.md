---
symbol: generoagentewidget
kind: class
module: personalizador/views/ajaxviews.py
lines: 14-16
signature_hash: sha1:3a52b3b5be43907c7bdf9bab7c5a4a6ae288be57
authored: true
---

# generoagentewidget

**Módulo:** `personalizador/views/ajaxviews.py` (líneas 14-16) · hereda de `AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir GeneroAgente vía búsqueda AJAX incremental — ver CLAUDE.md sobre `django-select2` y `carga/views/ajaxviews.py` (mismo patrón, definido allá). Catálogo chico (`SmallCatalogWidgetMixin`), con alta rápida (`personalizador:crear-generoagente`).

## Firma

```python
class generoagentewidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Agente.sexo`/`ComisionadoExterno.sexo` en sus respectivos forms.

## Ver también

- [GeneroAgente](../../models/GeneroAgente.md)
