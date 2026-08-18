---
symbol: EliminarTipoLicenciaPermiso
kind: class
module: personalizador/views/tipolicenciapermisoviews.py
lines: 12-17
signature_hash: sha1:5f2742345c0fe99b28803613350458c35cd286d1
authored: true
---

# EliminarTipoLicenciaPermiso

**Módulo:** `personalizador/views/tipolicenciapermisoviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un TipoLicenciaPermiso, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarTipoLicenciaPermiso(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de TipoLicenciaPermiso.

## Ver también

- [TipoLicenciaPermiso](../../models/TipoLicenciaPermiso.md)
