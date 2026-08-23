---
symbol: EliminarTituloProfesional
kind: class
module: personalizador/views/tituloprofesionalviews.py
lines: 12-17
signature_hash: sha1:6dd31bfc0042acdd20468db3b387e58394255aca
authored: true
---

# EliminarTituloProfesional

**Módulo:** `personalizador/views/tituloprofesionalviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un TituloProfesional, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarTituloProfesional(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de TituloProfesional.

## Ver también

- [TituloProfesional](../../models/TituloProfesional.md)
