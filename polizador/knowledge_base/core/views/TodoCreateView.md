---
symbol: TodoCreateView
kind: class
module: core/views.py
lines: 197-205
signature_hash: sha1:c973fee5192bbaf364771cf0da19ec98533182f9
authored: true
---
# TodoCreateView

**Módulo:** `core/views.py` (líneas 197-205) · hereda de `SuperuserRequiredMixin, CreateView`

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