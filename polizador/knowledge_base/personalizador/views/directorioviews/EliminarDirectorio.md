---
symbol: EliminarDirectorio
kind: class
module: personalizador/views/directorioviews.py
lines: 12-17
signature_hash: sha1:5cd4be47327944a983e5f2e5fcaf817f15df8259
authored: true
---

# EliminarDirectorio

**Módulo:** `personalizador/views/directorioviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un Directorio, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarDirectorio(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de Directorio.

## Ver también

- [Directorio](../../models/Directorio.md)
