---
symbol: EliminarActividadEspecifica
kind: class
module: personalizador/views/actividadespecificaviews.py
lines: 12-17
signature_hash: sha1:8e5544fd6cc2e88574ed1f413859f1055c558433
authored: true
---

# EliminarActividadEspecifica

**Módulo:** `personalizador/views/actividadespecificaviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un ActividadEspecifica, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarActividadEspecifica(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de ActividadEspecifica.

## Ver también

- [ActividadEspecifica](../../models/ActividadEspecifica.md)
