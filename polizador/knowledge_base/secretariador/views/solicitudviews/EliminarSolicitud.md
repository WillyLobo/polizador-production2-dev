---
symbol: EliminarSolicitud
kind: class
module: secretariador/views/solicitudviews.py
lines: 184-189
signature_hash: sha1:65c9bddd464e92247c0b46a8e5fc7bf4211b10f4
authored: true
---

# EliminarSolicitud

**Módulo:** `secretariador/views/solicitudviews.py` (líneas 184-189) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una Solicitud, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarSolicitud(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de Solicitud.

## Ver también

- [Solicitud](../../models/Solicitud.md)
