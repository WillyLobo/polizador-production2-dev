---
symbol: UpdateReceptor
kind: class
module: carga/views/receptorviews.py
lines: 41-47
signature_hash: sha1:506b696666c2130b687f465233f8d7156b1957ea
authored: true
---

# UpdateReceptor

**Módulo:** `carga/views/receptorviews.py` (líneas 41-47) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de Receptor vía `ModelForm` estándar.

## Firma

```python
class UpdateReceptor(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateReceptor` (`carga:update-receptor`), enlazada desde el listado/ficha.

## Ver también

- [Receptor](../../models/Receptor.md)
