---
symbol: UpdateRegion
kind: class
module: carga/views/regionviews.py
lines: 41-47
signature_hash: sha1:e8fa22edbe0942feef99a1e4591d8d188e7f7e72
authored: true
---

# UpdateRegion

**Módulo:** `carga/views/regionviews.py` (líneas 41-47) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de Region vía `ModelForm` estándar.

## Firma

```python
class UpdateRegion(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateRegion` (`carga:update-region`), enlazada desde el listado/ficha.

## Ver también

- [Region](../../models/Region.md)
