---
symbol: TodoListView
kind: class
module: core/views.py
lines: 181-190
signature_hash: sha1:379f3178610bc8544414b378317058b0e60dfd5e
authored: true
---

# TodoListView

**Módulo:** `core/views.py` (líneas 181-190) · hereda de `SuperuserRequiredMixin, ListView`

## Propósito

Listado de tareas pendientes, con el form de alta rápida (`TodoForm`) y los choices de estado en el contexto para el filtro/badge del template.

## Firma

```python
class TodoListView(SuperuserRequiredMixin, ListView):
```

## Uso real

`TodoListView` (`todo_list`), enlazada desde el navbar ("Administracion > Tareas pendientes").

## Ver también

- [Todo](../models/Todo.md)
