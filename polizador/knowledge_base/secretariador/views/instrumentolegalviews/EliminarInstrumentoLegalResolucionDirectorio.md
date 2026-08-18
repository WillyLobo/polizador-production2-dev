---
symbol: EliminarInstrumentoLegalResolucionDirectorio
kind: class
module: secretariador/views/instrumentolegalviews.py
lines: 168-173
signature_hash: sha1:125c437f2eb6254f184fefa6673b79bdaabf5a75
authored: true
---

# EliminarInstrumentoLegalResolucionDirectorio

**Módulo:** `secretariador/views/instrumentolegalviews.py` (líneas 168-173) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y ejecuta el borrado de una InstrumentosLegalesResoluciones (Directorio), mostrando antes (vía `DeleteRelatedObjectsMixin`
— `core/mixins.py` + `core/deletion.py::get_deleted_objects`) los objetos relacionados que
se borrarían en cascada.
 Mismo `permission_required` que la versión Presidencia (`delete_instrumentoslegalesresoluciones`) — son el mismo modelo, la distinción Presidencia/Directorio es solo de formulario/template, no de permisos.

## Firma

```python
class EliminarInstrumentoLegalResolucionDirectorio(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

Enlazada desde el listado de resoluciones.

## Ver también

- [InstrumentosLegalesResoluciones](../../models/InstrumentosLegalesResoluciones.md)
