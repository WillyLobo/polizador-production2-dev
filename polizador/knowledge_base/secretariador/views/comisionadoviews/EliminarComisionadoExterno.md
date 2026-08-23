---
symbol: EliminarComisionadoExterno
kind: class
module: secretariador/views/comisionadoviews.py
lines: 92-97
signature_hash: sha1:c7476b92c68f8e17c35b4be57f5c7493cb584a34
authored: true
---

# EliminarComisionadoExterno

**Módulo:** `secretariador/views/comisionadoviews.py` (líneas 92-97) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

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
