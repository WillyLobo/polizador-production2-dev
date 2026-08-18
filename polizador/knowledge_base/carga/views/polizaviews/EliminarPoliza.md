---
symbol: EliminarPoliza
kind: class
module: carga/views/polizaviews.py
lines: 13-18
signature_hash: sha1:efe6eafbac3d922ae2121b2c21815402c140886f
authored: true
---

# EliminarPoliza

**Módulo:** `carga/views/polizaviews.py` (líneas 13-18) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una Poliza, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarPoliza(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado/ficha de Póliza.

## Ver también

- [Poliza](../../models/Poliza.md)
