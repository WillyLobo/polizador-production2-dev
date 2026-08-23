---
symbol: EliminarReceptor
kind: class
module: carga/views/receptorviews.py
lines: 11-16
signature_hash: sha1:9165526bcde6ae270bcac6b80bfee18220dce1f7
authored: true
---

# EliminarReceptor

**Módulo:** `carga/views/receptorviews.py` (líneas 11-16) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un Receptor, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarReceptor(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado y la ficha de Receptor (botón de borrar de `polizador/context_processors.py::eliminarlinkimg`).

## Ver también

- [Receptor](../../models/Receptor.md)
