---
symbol: EliminarComisionadoExterno
kind: class
module: secretariador/views/comisionadoviews.py
lines: 56-61
signature_hash: sha1:703579b6e2f736ada34034bbd61b08b6b5a557f4
authored: true
---
# EliminarComisionadoExterno

**Módulo:** `secretariador/views/comisionadoviews.py` (líneas 56-61) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un ComisionadoExterno, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarComisionadoExterno(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado de comisionados externos.

## Ver también

- [ComisionadoExterno](../../../personalizador/models/ComisionadoExterno.md)