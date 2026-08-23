---
symbol: localidadwidget
kind: class
module: carga/views/ajaxviews.py
lines: 211-214
signature_hash: sha1:fd297fed14e0eb7d2f792bd1c534d0deb7e54103
authored: true
---

# localidadwidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 211-214) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Localidad vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Selección simple.

## Firma

```python
class localidadwidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

Campos `ForeignKey` a Localidad.

## Ver también

- [localidadmultiplewidget](localidadmultiplewidget.md)
