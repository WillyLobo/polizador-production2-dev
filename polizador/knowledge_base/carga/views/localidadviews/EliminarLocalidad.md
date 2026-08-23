---
symbol: EliminarLocalidad
kind: class
module: carga/views/localidadviews.py
lines: 12-17
signature_hash: sha1:570054f04cab3a7a43486f77e4c58647a4bfea08
authored: true
---

# EliminarLocalidad

**Módulo:** `carga/views/localidadviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una Localidad, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarLocalidad(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado y la ficha de Localidad (botón de borrar de `polizador/context_processors.py::eliminarlinkimg`).

## Ver también

- [Localidad](../../models/Localidad.md)
