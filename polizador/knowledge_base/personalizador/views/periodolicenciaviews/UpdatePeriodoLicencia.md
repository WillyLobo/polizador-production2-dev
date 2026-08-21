---
symbol: UpdatePeriodoLicencia
kind: class
module: personalizador/views/periodolicenciaviews.py
lines: 41-47
signature_hash: sha1:bffebf2210e5d4b75e4a7031e43e0dcd38d8c99a
authored: true
---

# UpdatePeriodoLicencia

**Módulo:** `personalizador/views/periodolicenciaviews.py` (líneas 41-47) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de `PeriodoLicencia` vía `ModelForm` estándar.

## Firma

```python
class UpdatePeriodoLicencia(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdatePeriodoLicencia` (`personalizador:update-periodolicencia`).

## Ver también

- [PeriodoLicencia](../../models/PeriodoLicencia.md)
- [PeriodoLicenciaForm](../../forms/periodolicenciaforms/PeriodoLicenciaForm.md)
