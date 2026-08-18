---
symbol: TodoForm
kind: class
module: core/forms.py
lines: 6-13
signature_hash: sha1:de93bf7e856b29a27f606a4aaf283cbefd4c751b
authored: true
---

# TodoForm

**Módulo:** `core/forms.py` (líneas 6-13) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` mínimo para `Todo` (título + descripción — el estado se maneja aparte).

## Firma

```python
class TodoForm(forms.ModelForm):
```

## Uso real

`TodoListView`/`TodoCreateView`/`TodoUpdateView` (`core/views.py`).

## Ver también

- [Todo](../models/Todo.md)
