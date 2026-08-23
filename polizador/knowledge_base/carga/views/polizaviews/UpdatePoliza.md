---
symbol: UpdatePoliza
kind: class
module: carga/views/polizaviews.py
lines: 43-51
signature_hash: sha1:b833728011b9e0cd425015f308bcc8668cd53ca1
authored: true
---

# UpdatePoliza

**Módulo:** `carga/views/polizaviews.py` (líneas 43-51) · hereda de `PermissionRequiredMixin, UserKwargsMixin, UserFormsetKwargsMixin, FormsetViewMixin, generic.UpdateView`

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
