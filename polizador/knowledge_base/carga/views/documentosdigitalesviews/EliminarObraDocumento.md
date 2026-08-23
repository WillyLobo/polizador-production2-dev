---
symbol: EliminarObraDocumento
kind: class
module: carga/views/documentosdigitalesviews.py
lines: 95-100
signature_hash: sha1:5f9c57396c93b7a9a882ad7741bd0980d44c725a
authored: true
---

# EliminarObraDocumento

**Módulo:** `carga/views/documentosdigitalesviews.py` (líneas 95-100) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un ObraDocumento, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarObraDocumento(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde la ficha de Obra.

## Ver también

- [ObraDocumento](../../models/ObraDocumento.md)
