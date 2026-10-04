---
symbol: TodoUpdateView
kind: class
module: core/views.py
lines: 231-235
signature_hash: sha1:340b28aee364d5a1f183ad1f391f87a2c17e1364
authored: true
---
# TodoUpdateView

**Módulo:** `core/views.py` (líneas 231-235) · hereda de `SuperuserRequiredMixin, UpdateView`

## Propósito

Edición de una tarea (título/descripción — el estado se cambia aparte, ver `TodoStatusUpdateView`).

## Firma

```python
class TodoUpdateView(SuperuserRequiredMixin, UpdateView):
```

## Uso real

`TodoUpdateView` (`todo_update`).

## Ver también

- [Todo](../models/Todo.md)