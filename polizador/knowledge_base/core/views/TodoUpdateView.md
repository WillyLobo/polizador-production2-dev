---
symbol: TodoUpdateView
kind: class
module: core/views.py
lines: 204-208
signature_hash: sha1:13d22dadb2caad3850d92a9ad14d77a7750362f0
authored: true
---

# TodoUpdateView

**Módulo:** `core/views.py` (líneas 204-208) · hereda de `SuperuserRequiredMixin, UpdateView`

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
