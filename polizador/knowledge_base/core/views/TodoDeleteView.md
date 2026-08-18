---
symbol: TodoDeleteView
kind: class
module: core/views.py
lines: 211-214
signature_hash: sha1:fdedf843495bd2fddeecd83e195c6462d7ae3c20
authored: true
---

# TodoDeleteView

**Módulo:** `core/views.py` (líneas 211-214) · hereda de `SuperuserRequiredMixin, DeleteView`

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
