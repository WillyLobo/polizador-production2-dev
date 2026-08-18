---
symbol: EliminarSolicitudExterior
kind: class
module: secretariador/views/solicitud_exteriorviews.py
lines: 283-288
signature_hash: sha1:0734a7c1f7a3a8515e28baa13d9101a7e4d9329b
authored: true
---

# EliminarSolicitudExterior

**Módulo:** `secretariador/views/solicitud_exteriorviews.py` (líneas 283-288) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una Solicitud (exterior), mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarSolicitudExterior(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de Solicitud Exterior.

## Ver también

- [Solicitud](../../models/Solicitud.md)
