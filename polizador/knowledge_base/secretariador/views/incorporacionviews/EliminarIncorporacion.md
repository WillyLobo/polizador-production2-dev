---
symbol: EliminarIncorporacion
kind: class
module: secretariador/views/incorporacionviews.py
lines: 266-271
signature_hash: sha1:79df2f220d64717c740dc3b8aff4acbd927bd620
authored: true
---

# EliminarIncorporacion

**Módulo:** `secretariador/views/incorporacionviews.py` (líneas 266-271) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una Incorporacion, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarIncorporacion(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de Incorporación.

## Ver también

- [Incorporacion](../../models/Incorporacion.md)
