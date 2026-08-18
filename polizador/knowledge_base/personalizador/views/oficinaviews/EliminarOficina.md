---
symbol: EliminarOficina
kind: class
module: personalizador/views/oficinaviews.py
lines: 12-17
signature_hash: sha1:6ad7f755f672c4f8c645ccb5c345d18c9979a8a4
authored: true
---

# EliminarOficina

**Módulo:** `personalizador/views/oficinaviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una Oficina, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarOficina(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de Oficina.

## Ver también

- [Oficina](../../models/Oficina.md)
