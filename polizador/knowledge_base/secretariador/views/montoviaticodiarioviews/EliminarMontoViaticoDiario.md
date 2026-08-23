---
symbol: EliminarMontoViaticoDiario
kind: class
module: secretariador/views/montoviaticodiarioviews.py
lines: 115-120
signature_hash: sha1:bfd377037aa48d9e22eab84d6cf8faf6eac9a142
authored: true
---

# EliminarMontoViaticoDiario

**Módulo:** `secretariador/views/montoviaticodiarioviews.py` (líneas 115-120) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un MontoViaticoDiario, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarMontoViaticoDiario(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado de decretos.

## Ver también

- [MontoViaticoDiario](../../models/MontoViaticoDiario.md)
