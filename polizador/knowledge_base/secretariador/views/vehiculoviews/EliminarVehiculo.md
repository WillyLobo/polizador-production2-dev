---
symbol: EliminarVehiculo
kind: class
module: secretariador/views/vehiculoviews.py
lines: 41-46
signature_hash: sha1:f646c078d98eefe0277f294a7bb988bb66a67667
authored: true
---

# EliminarVehiculo

**Módulo:** `secretariador/views/vehiculoviews.py` (líneas 41-46) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un Vehiculo, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarVehiculo(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado de vehículos.

## Ver también

- [Vehiculo](../../models/Vehiculo.md)
