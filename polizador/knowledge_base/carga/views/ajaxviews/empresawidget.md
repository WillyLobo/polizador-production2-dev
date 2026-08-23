---
symbol: empresawidget
kind: class
module: carga/views/ajaxviews.py
lines: 178-182
signature_hash: sha1:51372dd33f4d51946a838d05883c9d515670204f
authored: true
---

# empresawidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 178-182) · hereda de `AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Empresa vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Con alta rápida (`carga:crear-empresa`).

## Firma

```python
class empresawidget(AddRelatedWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`Obra.obra_empresa`, `Poliza.poliza_tomador`.

## Ver también

- [Empresa](../../models/Empresa.md)
