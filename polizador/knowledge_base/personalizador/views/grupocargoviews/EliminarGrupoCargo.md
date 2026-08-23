---
symbol: EliminarGrupoCargo
kind: class
module: personalizador/views/grupocargoviews.py
lines: 12-17
signature_hash: sha1:6fd3e0562eeb11663c8aec4acd3137a28ee8893c
authored: true
---

# EliminarGrupoCargo

**Módulo:** `personalizador/views/grupocargoviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un GrupoCargo, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarGrupoCargo(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de GrupoCargo.

## Ver también

- [GrupoCargo](../../models/GrupoCargo.md)
