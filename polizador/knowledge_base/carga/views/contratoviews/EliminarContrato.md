---
symbol: EliminarContrato
kind: class
module: carga/views/contratoviews.py
lines: 47-54
signature_hash: sha1:9b6776cec48e0d80cb47796706b51beb8f843fa1
authored: true
---

# EliminarContrato

**Módulo:** `carga/views/contratoviews.py` (líneas 47-54) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un Contrato, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.
 `get_success_url` vuelve a la ficha de la Obra dueña.

## Firma

```python
class EliminarContrato(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde la ficha de Obra.

## Ver también

- [Contrato](../../models/Contrato.md)
