---
symbol: localidadmultiplewidget
kind: class
module: carga/views/ajaxviews.py
lines: 206-209
signature_hash: sha1:a625642367c388497d11c216ad718fa7939110fd
authored: true
---

# localidadmultiplewidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 206-209) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Localidad vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Selección múltiple.

## Firma

```python
class localidadmultiplewidget(LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
```

## Uso real

`Obra.obra_localidad_m` en `ObraForm`.

## Ver también

- [Localidad](../../models/Localidad.md)
