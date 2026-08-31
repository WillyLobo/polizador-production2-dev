---
symbol: TodoDeleteView
kind: class
module: core/views.py
lines: 215-218
signature_hash: sha1:96b17b66cb6f093c1e1cab43a3ffde65a75a2524
authored: true
---
# TodoDeleteView

**Módulo:** `core/views.py` (líneas 215-218) · hereda de `SuperuserRequiredMixin, DeleteView`

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