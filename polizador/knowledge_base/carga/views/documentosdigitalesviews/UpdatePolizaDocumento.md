---
symbol: UpdatePolizaDocumento
kind: class
module: carga/views/documentosdigitalesviews.py
lines: 143-151
signature_hash: sha1:216d630cc8ff529f519ca1fcfb39b55f5adc0c1d
authored: true
---

# UpdatePolizaDocumento

**Módulo:** `carga/views/documentosdigitalesviews.py` (líneas 143-151) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de un `PolizaDocumento` (descripción o reemplazo del PDF). Exige
`carga.change_polizadocumento` y vuelve a la ficha de la Póliza.

## Firma

```python
class UpdatePolizaDocumento(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`carga:update-poliza-documento`, desde la ficha de la Póliza.

## Ver también

- [PolizaDocumento](../../models/PolizaDocumento.md)
- [CrearPolizaDocumento](CrearPolizaDocumento.md)
