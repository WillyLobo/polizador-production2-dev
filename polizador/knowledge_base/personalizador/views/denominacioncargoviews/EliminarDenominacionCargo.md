---
symbol: EliminarDenominacionCargo
kind: class
module: personalizador/views/denominacioncargoviews.py
lines: 12-17
signature_hash: sha1:351d85fcda1b948f078711b02af822fbc62df85e
authored: true
---

# EliminarDenominacionCargo

**Módulo:** `personalizador/views/denominacioncargoviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un DenominacionCargo, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarDenominacionCargo(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de DenominacionCargo.

## Ver también

- [DenominacionCargo](../../models/DenominacionCargo.md)
