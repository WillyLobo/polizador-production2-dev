---
symbol: UpdateLicenciaPermiso
kind: class
module: personalizador/views/licenciapermisoviews.py
lines: 63-71
signature_hash: sha1:ac42265910a32e9c095c36733be77a3d9bf871f0
authored: true
---

# UpdateLicenciaPermiso

**Módulo:** `personalizador/views/licenciapermisoviews.py` (líneas 63-71) · hereda de `PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView`

## Propósito

Edición de LicenciaPermiso + formset de devoluciones de horas.

## Firma

```python
class UpdateLicenciaPermiso(PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView):
```

## Uso real

`UpdateLicenciaPermiso` (`personalizador:update-licenciapermiso`).

## Ver también

- [LicenciaPermiso](../../models/LicenciaPermiso.md)
