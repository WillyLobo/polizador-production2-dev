---
symbol: EliminarLicenciaPermiso
kind: class
module: personalizador/views/licenciapermisoviews.py
lines: 18-23
signature_hash: sha1:c4b90f81c40885ded86b6382d5df8eb50b2fd459
authored: true
---

# EliminarLicenciaPermiso

**Módulo:** `personalizador/views/licenciapermisoviews.py` (líneas 18-23) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una LicenciaPermiso, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarLicenciaPermiso(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha.

## Ver también

- [LicenciaPermiso](../../models/LicenciaPermiso.md)
