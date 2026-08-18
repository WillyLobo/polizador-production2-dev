---
symbol: Todo
kind: class
module: core/models.py
lines: 78-113
signature_hash: sha1:2c3a167116163b83bf2cd826d66b9611cb910fc8
authored: true
---

# Todo

**Módulo:** `core/models.py` (líneas 78-113) · hereda de `models.Model`

## Propósito

Una tarea pendiente del panel `/administracion/tareas/` — el reemplazo estructurado del `TODO.md` histórico del repo (ver `core/management/commands/seed_todos.py`, que migró las tareas de ese archivo a esta tabla una sola vez). `status_badge` mapea cada `Status` a una clase de color Bootstrap para el listado.

## Firma

```python
class Todo(models.Model):
```

## Uso real

`TodoListView`/`TodoCreateView`/`TodoUpdateView`/`TodoDeleteView`/`TodoStatusUpdateView` (`core/views.py`).

## Ver también

- [TodoListView](../views/TodoListView.md)
