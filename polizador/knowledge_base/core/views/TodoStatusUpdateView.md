---
symbol: TodoStatusUpdateView
kind: class
module: core/views.py
lines: 217-226
signature_hash: sha1:50ebd4fd472216e4c113320ef676f365649aac03
authored: true
---

# TodoStatusUpdateView

**Módulo:** `core/views.py` (líneas 217-226) · hereda de `SuperuserRequiredMixin, View`

## Propósito

Cambia solo el `status` de una tarea (`save(update_fields=["status", "updated_at"])`, no todos los campos) — pensada para un botón/dropdown rápido en el listado, sin pasar por el form completo de edición. Valida el valor contra `Todo.Status.values` antes de guardar.

## Firma

```python
class TodoStatusUpdateView(SuperuserRequiredMixin, View):
```

## Uso real

`TodoStatusUpdateView` (`todo_status_update`), enlazada desde `TodoListView`.

## Ver también

- [Todo](../models/Todo.md)
- [TodoListView](TodoListView.md)
