---
symbol: EliminarDireccion
kind: class
module: personalizador/views/direccionviews.py
lines: 12-17
signature_hash: sha1:4be41b445423f2b3120f133a3edf0c5ce09234dc
authored: true
---

# EliminarDireccion

**Módulo:** `personalizador/views/direccionviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una Direccion, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarDireccion(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de Direccion.

## Ver también

- [Direccion](../../models/Direccion.md)
