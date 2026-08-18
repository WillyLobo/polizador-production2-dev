---
symbol: EliminarCargoTipo
kind: class
module: personalizador/views/cargotipoviews.py
lines: 12-17
signature_hash: sha1:0af8a6c36e3ae0277ba1cd3244478a0e9efb28a7
authored: true
---

# EliminarCargoTipo

**Módulo:** `personalizador/views/cargotipoviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un CargoTipo, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarCargoTipo(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de CargoTipo.

## Ver también

- [CargoTipo](../../models/CargoTipo.md)
