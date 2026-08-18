---
symbol: UpdateArea
kind: class
module: carga/views/areaviews.py
lines: 30-36
signature_hash: sha1:7660be42d0b00c9f2e303c956c8c0c08dcb34cd7
authored: true
---

# UpdateArea

**Módulo:** `carga/views/areaviews.py` (líneas 30-36) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de Area vía `ModelForm` estándar.

## Firma

```python
class UpdateArea(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateArea` (`carga:update-area`), enlazada desde el listado/ficha.

## Ver también

- [Area](../../models/Area.md)
