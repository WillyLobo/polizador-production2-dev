---
symbol: EliminarTextoResolucion
kind: class
module: carga/views/textoresolucionviews.py
lines: 144-149
signature_hash: sha1:ed20111a7dba4ea657ce126e8685c5d1cbd40470
authored: true
---

# EliminarTextoResolucion

**Módulo:** `carga/views/textoresolucionviews.py` (líneas 144-149) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y borra una plantilla, mostrando antes lo que se borraría en cascada
(`DeleteRelatedObjectsMixin`). Los certificados no tienen FK a la plantilla: sus snapshots
guardan sólo `textoresolucion_id`, así que sobreviven al borrado. Exige
`carga.delete_textoresolucioncertificado` y vuelve al listado.

## Firma

```python
class EliminarTextoResolucion(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

`carga:eliminar-texto-resolucion`, desde el listado.

## Ver también

- [TextoResolucionCertificado](../../models/TextoResolucionCertificado.md)
