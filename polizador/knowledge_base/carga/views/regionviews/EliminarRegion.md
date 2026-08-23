---
symbol: EliminarRegion
kind: class
module: carga/views/regionviews.py
lines: 12-17
signature_hash: sha1:cffe2cc5f492c020ab46adf6c8991a96dd37d5ea
authored: true
---

# EliminarRegion

**Módulo:** `carga/views/regionviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una Region, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarRegion(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado y la ficha de Region (botón de borrar de `polizador/context_processors.py::eliminarlinkimg`).

## Ver también

- [Region](../../models/Region.md)
