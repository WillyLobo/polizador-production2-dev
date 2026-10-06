---
symbol: UpdatePoliza
kind: class
module: carga/views/polizaviews.py
lines: 65-73
signature_hash: sha1:fedd1a3a22917c80f0f015ba154abc8cf2649d1a
authored: true
---

# UpdatePoliza

**Módulo:** `carga/views/polizaviews.py` (líneas 65-73) · hereda de `PermissionRequiredMixin, UserKwargsMixin, UserFormsetKwargsMixin, FormsetViewMixin, generic.UpdateView`

## Propósito

Edición de Póliza + formset de movimientos (se pueden agregar movimientos nuevos sin crear otra Póliza).

## Firma

```python
class UpdatePoliza(PermissionRequiredMixin, UserKwargsMixin, UserFormsetKwargsMixin, FormsetViewMixin, generic.UpdateView):
```

## Uso real

`UpdatePoliza` (`carga:update-poliza`).

## Ver también

- [Poliza](../../models/Poliza.md)
