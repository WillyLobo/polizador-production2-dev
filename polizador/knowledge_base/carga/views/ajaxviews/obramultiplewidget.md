---
symbol: obramultiplewidget
kind: class
module: carga/views/ajaxviews.py
lines: 184-189
signature_hash: sha1:061c972bed79cb9615d1262d1a7ce1f8176949e8
authored: true
---

# obramultiplewidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 184-189) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Obra vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Selección múltiple, mismos `search_fields` que `obrawidget`.

## Firma

```python
class obramultiplewidget(LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
```

## Uso real

`Obra.obra_principal` (`ManyToManyField` a sí misma, "Obra Madre").

## Ver también

- [obrawidget](obrawidget.md)
