---
symbol: CrearTipoLicenciaPermiso
kind: class
module: personalizador/views/tipolicenciapermisoviews.py
lines: 21-38
signature_hash: sha1:b0f3ddd779e6b8d478d18237affac99db3c610fa
authored: true
---

# CrearTipoLicenciaPermiso

**Módulo:** `personalizador/views/tipolicenciapermisoviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de TipoLicenciaPermiso vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir.

## Firma

```python
class CrearTipoLicenciaPermiso(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearTipoLicenciaPermiso` (`personalizador:crear-tipolicenciapermiso`).

## Ver también

- [TipoLicenciaPermiso](../../models/TipoLicenciaPermiso.md)
