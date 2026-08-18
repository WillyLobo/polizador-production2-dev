---
symbol: EliminarPolizaMovimiento
kind: class
module: carga/views/polizaviews.py
lines: 54-58
signature_hash: sha1:b30f17a7dadbf42fd5a8a154f2627a3628aaa68b
authored: true
---

# EliminarPolizaMovimiento

**Módulo:** `carga/views/polizaviews.py` (líneas 54-58) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un Poliza_Movimiento, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarPolizaMovimiento(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde la ficha de Póliza.

## Ver también

- [Poliza_Movimiento](../../models/Poliza_Movimiento.md)
