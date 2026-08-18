---
symbol: EliminarFojaDeMedicion
kind: class
module: carga/views/fojademedicionviews.py
lines: 252-259
signature_hash: sha1:b0de2995cece520740e001a1a67039beda3a1a31
authored: true
---

# EliminarFojaDeMedicion

**Módulo:** `carga/views/fojademedicionviews.py` (líneas 252-259) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una FojaDeMedicion, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.
 `get_success_url` (no `success_url` fijo) redirige a la ficha de la Obra dueña, resuelta desde `foja_rubro` — no hay una URL de "lista de fojas" a la que volver.

## Firma

```python
class EliminarFojaDeMedicion(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde la ficha de la Foja.

## Ver también

- [FojaDeMedicion](../../models/FojaDeMedicion.md)
