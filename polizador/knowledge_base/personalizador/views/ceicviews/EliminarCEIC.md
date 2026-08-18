---
symbol: EliminarCEIC
kind: class
module: personalizador/views/ceicviews.py
lines: 12-17
signature_hash: sha1:7821026b9ba4eaf77332b5bf0b18c797f3ea8711
authored: true
---

# EliminarCEIC

**Módulo:** `personalizador/views/ceicviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un CEIC, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarCEIC(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de CEIC.

## Ver también

- [CEIC](../../models/CEIC.md)
