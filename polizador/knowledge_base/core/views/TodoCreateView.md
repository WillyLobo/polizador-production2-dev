---
symbol: TodoCreateView
kind: class
module: core/views.py
lines: 193-201
signature_hash: sha1:0a69e0baea8999d50f678d7d274fb864458bf07e
authored: true
---

# TodoCreateView

**Módulo:** `core/views.py` (líneas 193-201) · hereda de `SuperuserRequiredMixin, CreateView`

## Propósito

Alta de una tarea, seteando `created_by` al usuario logueado en `form_valid` (no expuesto como campo del form — se infiere de la sesión).

## Firma

```python
class TodoCreateView(SuperuserRequiredMixin, CreateView):
```

## Uso real

`TodoCreateView` (`todo_create`).

## Ver también

- [Todo](../models/Todo.md)
