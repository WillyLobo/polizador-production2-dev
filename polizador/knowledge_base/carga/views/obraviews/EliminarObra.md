---
symbol: EliminarObra
kind: class
module: carga/views/obraviews.py
lines: 63-68
signature_hash: sha1:46b38a1fe86774eb78bd9097671f7ef6ca6ce6bf
authored: true
---

# EliminarObra

**Módulo:** `carga/views/obraviews.py` (líneas 63-68) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una Obra, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarObra(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de Obra.

## Ver también

- [Obra](../../models/Obra.md)
