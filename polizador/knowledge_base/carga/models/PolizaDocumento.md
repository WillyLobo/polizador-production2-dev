---
symbol: PolizaDocumento
kind: class
module: carga/models.py
lines: 283-296
signature_hash: sha1:f9fb9c75081b538442f8ab3c1bb3cb5192653440
authored: true
---

# PolizaDocumento

**Módulo:** `carga/models.py` (líneas 283-296) · hereda de `models.Model`

## Propósito

Un PDF adicional adjunto a una Póliza: anexos, adendas de cobertura, etc. Antes la
Póliza sólo admitía un archivo (`poliza_digital`). Cada documento lleva una
`polizadocumento_descripcion` libre (ej. "Anexo N°1") y el archivo, validado como PDF de
hasta 14 MB con `FileValidator`, igual que el resto de los adjuntos de `carga`. El nombre
en el storage sale del UUID ([generate_name_poliza_documento](generate_name_poliza_documento.md)),
no del nombre que subió el usuario. Se borra en cascada con la Póliza
(`related_name="documentos_poliza"`) y tiene historial propio.

## Firma

```python
class PolizaDocumento(models.Model):
```

## Uso real

Se lista en la ficha de la Póliza (`poliza.documentos_poliza`) y se gestiona con
[CrearPolizaDocumento](../views/documentosdigitalesviews/CrearPolizaDocumento.md)/[UpdatePolizaDocumento](../views/documentosdigitalesviews/UpdatePolizaDocumento.md)/[EliminarPolizaDocumento](../views/documentosdigitalesviews/EliminarPolizaDocumento.md).

## Ver también

- [Poliza](Poliza.md)
- [PolizaDocumentoForm](../forms/documentosdigitalesforms/PolizaDocumentoForm.md)
- [generate_name_poliza_documento](generate_name_poliza_documento.md)
