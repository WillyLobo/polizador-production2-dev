---
symbol: TodoUpdateView
kind: class
module: core/views.py
lines: 208-212
signature_hash: sha1:6b6b842923c9f636eff945ae198055a269ccf584
authored: true
---
# TodoUpdateView

**Módulo:** `core/views.py` (líneas 208-212) · hereda de `SuperuserRequiredMixin, UpdateView`

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