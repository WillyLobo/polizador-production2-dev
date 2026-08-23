---
symbol: rubrowidget
kind: class
module: carga/views/ajaxviews.py
lines: 76-80
signature_hash: sha1:4031d29d50dc533d6ad36f297f89435d57760049
authored: true
---

# rubrowidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 76-80) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) PlanDeTrabajosRubro vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Busca por nombre de rubro y por la Obra del plan.

## Firma

```python
class rubrowidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

Selección de Rubro en formularios que lo referencian (ej. `FojaDeMedicionForm`).

## Ver también

- [PlanDeTrabajosRubro](../../models/PlanDeTrabajosRubro.md)
