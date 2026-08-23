---
symbol: EliminarCategoria
kind: class
module: personalizador/views/categoriaviews.py
lines: 12-17
signature_hash: sha1:2fa22eb5da77b41463970be9091a5336ea221020
authored: true
---

# EliminarCategoria

**Módulo:** `personalizador/views/categoriaviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una Categoria, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarCategoria(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de Categoria.

## Ver también

- [Categoria](../../models/Categoria.md)
