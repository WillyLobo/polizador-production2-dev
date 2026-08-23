---
symbol: EliminarConjunto
kind: class
module: carga/views/conjuntoviews.py
lines: 12-17
signature_hash: sha1:8b9867c94152f69f29ce607e8db64d79e117fc7e
authored: true
---

# EliminarConjunto

**Módulo:** `carga/views/conjuntoviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un ConjuntoLicitado, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarConjunto(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado y la ficha de ConjuntoLicitado (botón de borrar de `polizador/context_processors.py::eliminarlinkimg`).

## Ver también

- [ConjuntoLicitado](../../models/ConjuntoLicitado.md)
