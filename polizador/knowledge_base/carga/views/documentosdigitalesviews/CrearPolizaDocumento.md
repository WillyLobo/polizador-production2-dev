---
symbol: CrearPolizaDocumento
kind: class
module: carga/views/documentosdigitalesviews.py
lines: 115-140
signature_hash: sha1:a47a51386b14ea3589cad9cd0147123d5df70dbb
authored: true
---

# CrearPolizaDocumento

**Módulo:** `carga/views/documentosdigitalesviews.py` (líneas 115-140) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de un [PolizaDocumento](../../models/PolizaDocumento.md) (anexo/adenda en PDF). Si
viene `?poliza=<id>`, precarga la Póliza destino. Exige `carga.add_polizadocumento` y al
terminar vuelve a la ficha de la Póliza (`carga:estado-poliza`).

## Firma

```python
class CrearPolizaDocumento(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`carga:crear-poliza-documento`, enlazada desde la ficha de la Póliza con `?poliza=<pk>`.

## Ver también

- [PolizaDocumento](../../models/PolizaDocumento.md)
- [PolizaDocumentoForm](../../forms/documentosdigitalesforms/PolizaDocumentoForm.md)
- [UpdatePolizaDocumento](UpdatePolizaDocumento.md)
