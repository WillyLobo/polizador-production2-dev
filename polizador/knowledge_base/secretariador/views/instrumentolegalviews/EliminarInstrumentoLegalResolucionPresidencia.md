---
symbol: EliminarInstrumentoLegalResolucionPresidencia
kind: class
module: secretariador/views/instrumentolegalviews.py
lines: 160-165
signature_hash: sha1:385439c3c55ea895caf698615092471cfc4426ad
authored: true
---

# EliminarInstrumentoLegalResolucionPresidencia

**Módulo:** `secretariador/views/instrumentolegalviews.py` (líneas 160-165) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una InstrumentosLegalesResoluciones (Presidencia), mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.

## Firma

```python
class EliminarInstrumentoLegalResolucionPresidencia(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado de resoluciones.

## Ver también

- [InstrumentosLegalesResoluciones](../../models/InstrumentosLegalesResoluciones.md)
