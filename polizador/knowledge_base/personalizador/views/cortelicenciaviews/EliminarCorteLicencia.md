---
symbol: EliminarCorteLicencia
kind: class
module: personalizador/views/cortelicenciaviews.py
lines: 61-68
signature_hash: sha1:96ec49c69b92880954aa162ad15451cb5fb18cc8
authored: true
---

# EliminarCorteLicencia

**Módulo:** `personalizador/views/cortelicenciaviews.py` (líneas 61-68) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un CorteLicencia, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.
 `get_success_url` vuelve a la ficha de la LicenciaPermiso interrumpida.

## Firma

```python
class EliminarCorteLicencia(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde la ficha de la LicenciaPermiso.

## Ver también

- [CorteLicencia](../../models/CorteLicencia.md)
