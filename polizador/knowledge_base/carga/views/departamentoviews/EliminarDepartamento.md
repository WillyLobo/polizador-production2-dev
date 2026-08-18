---
symbol: EliminarDepartamento
kind: class
module: carga/views/departamentoviews.py
lines: 12-17
signature_hash: sha1:0c8331fd62247187b7b4adeb44e035e22c231c1a
authored: true
---

# EliminarDepartamento

**Módulo:** `carga/views/departamentoviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un Departamento, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarDepartamento(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado y la ficha de Departamento (botón de borrar de `polizador/context_processors.py::eliminarlinkimg`).

## Ver también

- [Departamento](../../models/Departamento.md)
