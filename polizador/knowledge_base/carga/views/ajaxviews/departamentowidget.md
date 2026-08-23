---
symbol: departamentowidget
kind: class
module: carga/views/ajaxviews.py
lines: 201-204
signature_hash: sha1:f88b338fd34bbba6be80070ad7699159175cc948
authored: true
---

# departamentowidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 201-204) · hereda de `SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Departamento vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Catálogo chico, selección simple.

## Firma

```python
class departamentowidget(SmallCatalogWidgetMixin, LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

Campos `ForeignKey`/selección simple a Departamento (ej. `Localidad.localidad_departamento`).

## Ver también

- [Departamento](../../models/Departamento.md)
