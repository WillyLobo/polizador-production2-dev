---
symbol: TodoListView
kind: class
module: core/views.py
lines: 185-194
signature_hash: sha1:df31abaaa66880ed536cfad41bdf3b2a37ec6a2b
authored: true
---
# TodoListView

**Módulo:** `core/views.py` (líneas 185-194) · hereda de `SuperuserRequiredMixin, ListView`

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