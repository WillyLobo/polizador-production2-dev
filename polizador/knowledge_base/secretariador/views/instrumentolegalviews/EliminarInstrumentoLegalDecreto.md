---
symbol: EliminarInstrumentoLegalDecreto
kind: class
module: secretariador/views/instrumentolegalviews.py
lines: 152-157
signature_hash: sha1:c0c0cb179ebec61385af59d42bb9d80777d0b5fd
authored: true
---

# EliminarInstrumentoLegalDecreto

**Módulo:** `secretariador/views/instrumentolegalviews.py` (líneas 152-157) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un InstrumentosLegalesDecretos, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarInstrumentoLegalDecreto(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado de decretos.

## Ver también

- [InstrumentosLegalesDecretos](../../models/InstrumentosLegalesDecretos.md)
