---
symbol: TodoListView
kind: class
module: core/views.py
lines: 208-217
signature_hash: sha1:ed488a374df82b8f77fc5ab2cf3279b36c96bba9
authored: true
---
# TodoListView

**Módulo:** `core/views.py` (líneas 208-217) · hereda de `SuperuserRequiredMixin, ListView`

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