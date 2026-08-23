---
symbol: EliminarApartadoCargo
kind: class
module: personalizador/views/apartadocargoviews.py
lines: 12-17
signature_hash: sha1:3caff0a711467992656781786a637abc5af49431
authored: true
---

# EliminarApartadoCargo

**Módulo:** `personalizador/views/apartadocargoviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un ApartadoCargo, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarApartadoCargo(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de ApartadoCargo.

## Ver también

- [ApartadoCargo](../../models/ApartadoCargo.md)
