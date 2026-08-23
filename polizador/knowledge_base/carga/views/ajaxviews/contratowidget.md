---
symbol: contratowidget
kind: class
module: carga/views/ajaxviews.py
lines: 244-248
signature_hash: sha1:f5caea657dfdbb0fb53391972fb0787494513d53
authored: true
---

# contratowidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 244-248) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Contrato vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Busca por descripción y por la Obra dueña.

## Firma

```python
class contratowidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

`PlanDeTrabajos.trabajos_contrato` en `PlandeTrabajoForm`.

## Ver también

- [Contrato](../../models/Contrato.md)
