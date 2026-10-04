---
symbol: TodoDeleteView
kind: class
module: core/views.py
lines: 238-241
signature_hash: sha1:3ef1b976839d3b379e2da332b74b7c4d60f7c995
authored: true
---
# TodoDeleteView

**Módulo:** `core/views.py` (líneas 238-241) · hereda de `SuperuserRequiredMixin, DeleteView`

## Propósito

Borrado de una tarea (sin `DeleteRelatedObjectsMixin` — `Todo` no tiene relaciones que en cascada valga la pena mostrar).

## Firma

```python
class TodoDeleteView(SuperuserRequiredMixin, DeleteView):
```

## Uso real

`TodoDeleteView` (`todo_delete`).

## Ver también

- [Todo](../models/Todo.md)