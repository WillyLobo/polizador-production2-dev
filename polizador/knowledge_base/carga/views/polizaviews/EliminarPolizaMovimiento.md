---
symbol: EliminarPolizaMovimiento
kind: class
module: carga/views/polizaviews.py
lines: 117-124
signature_hash: sha1:a2e98e4065372cf4e821d55a9de4ef39539b425a
authored: true
---

# EliminarPolizaMovimiento

**Módulo:** `carga/views/polizaviews.py` (líneas 117-124) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un Poliza_Movimiento, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

Al terminar vuelve a la ficha de la Póliza (`carga:estado-poliza`).

## Firma

```python
class EliminarPolizaMovimiento(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde la ficha de Póliza.

## Ver también

- [Poliza_Movimiento](../../models/Poliza_Movimiento.md)

- [CrearPolizaMovimiento](CrearPolizaMovimiento.md)
- [UpdatePolizaMovimiento](UpdatePolizaMovimiento.md)
