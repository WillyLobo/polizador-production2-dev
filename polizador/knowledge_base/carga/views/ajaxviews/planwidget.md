---
symbol: planwidget
kind: class
module: carga/views/ajaxviews.py
lines: 71-74
signature_hash: sha1:563bc77db94a9ea373b809e30f4e58a35e6e3bdc
authored: true
---

# planwidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 71-74) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) PlanDeTrabajos vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Busca por el nombre de la Obra dueña del plan.

## Firma

```python
class planwidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

Selección de Plan de Trabajos en formularios que lo referencian.

## Ver también

- [PlanDeTrabajos](../../models/PlanDeTrabajos.md)
