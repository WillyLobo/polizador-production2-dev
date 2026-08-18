---
symbol: EliminarContratoDigital
kind: class
module: carga/views/documentosdigitalesviews.py
lines: 52-57
signature_hash: sha1:dea8949435227242b751e6973d58d79e3c539fec
authored: true
---

# EliminarContratoDigital

**Módulo:** `carga/views/documentosdigitalesviews.py` (líneas 52-57) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un ContratosDigitales, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada, para que el usuario no borre a ciegas.

## Firma

```python
class EliminarContratoDigital(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde la ficha de Obra/Contrato.

## Ver también

- [ContratosDigitales](../../models/ContratosDigitales.md)
