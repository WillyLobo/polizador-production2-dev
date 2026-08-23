---
symbol: EliminarRepresentanteTecnico
kind: class
module: carga/views/representantetecnicoviews.py
lines: 12-17
signature_hash: sha1:e24fbee4e9abacc884a297f20bb5d41f9135ed72
authored: true
---

# EliminarRepresentanteTecnico

**Módulo:** `carga/views/representantetecnicoviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un RepresentanteTecnico, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarRepresentanteTecnico(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado y la ficha de RepresentanteTecnico (botón de borrar de `polizador/context_processors.py::eliminarlinkimg`).

## Ver también

- [RepresentanteTecnico](../../models/RepresentanteTecnico.md)
