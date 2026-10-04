---
symbol: EliminarPolizaDocumento
kind: class
module: carga/views/documentosdigitalesviews.py
lines: 154-161
signature_hash: sha1:ab0b1d38d9b732f58ef60391d97bd2a9e26990b9
authored: true
---

# EliminarPolizaDocumento

**Módulo:** `carga/views/documentosdigitalesviews.py` (líneas 154-161) · hereda de `PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView`

## Propósito

Confirma y borra un `PolizaDocumento`, mostrando antes los objetos relacionados que se
borrarían en cascada (`DeleteRelatedObjectsMixin`). Exige `carga.delete_polizadocumento` y
vuelve a la ficha de la Póliza.

## Firma

```python
class EliminarPolizaDocumento(PermissionRequiredMixin, DeleteRelatedObjectsMixin, generic.DeleteView):
```

## Uso real

`carga:eliminar-poliza-documento`, desde la ficha de la Póliza.

## Ver también

- [PolizaDocumento](../../models/PolizaDocumento.md)
