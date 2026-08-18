---
symbol: EliminarInstrumentoLegalMemorandum
kind: class
module: secretariador/views/instrumentolegalviews.py
lines: 144-149
signature_hash: sha1:aaec0ad5d16904c87005380d6868addf36a9d747
authored: true
---

# EliminarInstrumentoLegalMemorandum

**Módulo:** `secretariador/views/instrumentolegalviews.py` (líneas 144-149) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de un InstrumentosLegalesMemorandum, mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarInstrumentoLegalMemorandum(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado de memorandums.

## Ver también

- [InstrumentosLegalesMemorandum](../../models/InstrumentosLegalesMemorandum.md)
