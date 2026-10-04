---
symbol: TodoCreateView
kind: class
module: core/views.py
lines: 220-228
signature_hash: sha1:dd60026c3178beb115190bd2b0e70ad79a3223fc
authored: true
---
# TodoCreateView

**Módulo:** `core/views.py` (líneas 220-228) · hereda de `SuperuserRequiredMixin, CreateView`

## Propósito

Alta de una tarea, seteando `created_by` al usuario logueado en `form_valid` (no expuesto como campo del form — se infiere de la sesión).

## Firma

```python
class TodoCreateView(SuperuserRequiredMixin, CreateView):
```

## Uso real

`TodoCreateView` (`todo_create`).

## Ver también

- [Todo](../models/Todo.md)