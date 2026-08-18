---
symbol: aseguradorawidget
kind: class
module: carga/views/ajaxviews.py
lines: 151-155
signature_hash: sha1:cdeaf42e798c8aadfe1e7af49d01dc8dd1e47bcc
authored: true
---

# aseguradorawidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 151-155) · hereda de `AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Aseguradora vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Catálogo chico, con alta rápida (`carga:crear-aseguradora`).

## Firma

```python
class aseguradorawidget(AddRelatedWidgetMixin, SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Poliza.poliza_aseguradora` en `PolizaForm`.

## Ver también

- [Aseguradora](../../models/Aseguradora.md)
