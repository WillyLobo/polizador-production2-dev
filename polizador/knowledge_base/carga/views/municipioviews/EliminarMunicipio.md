---
symbol: EliminarMunicipio
kind: class
module: carga/views/municipioviews.py
lines: 12-17
signature_hash: sha1:799ba26e8410e717d5a40cc670a1a363e695a225
authored: true
---

# EliminarMunicipio

**Módulo:** `carga/views/municipioviews.py` (líneas 12-17) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un Municipio, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarMunicipio(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado y la ficha de Municipio (botón de borrar de `polizador/context_processors.py::eliminarlinkimg`).

## Ver también

- [Municipio](../../models/Municipio.md)
