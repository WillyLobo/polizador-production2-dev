---
symbol: EliminarDepartamento
kind: class
module: personalizador/views/departamentoviews.py
lines: 12-17
signature_hash: sha1:0c8331fd62247187b7b4adeb44e035e22c231c1a
authored: true
---

# EliminarDepartamento

**Módulo:** `personalizador/views/departamentoviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un Departamento, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarDepartamento(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de Departamento.

## Ver también

- [Departamento](../../models/Departamento.md)
