---
symbol: PolizaDocumentoForm
kind: class
module: carga/forms/documentosdigitalesforms.py
lines: 39-53
signature_hash: sha1:3b7c95e3408af3f4c10cb744a9a8c024e80500da
authored: true
---

# PolizaDocumentoForm

**Módulo:** `carga/forms/documentosdigitalesforms.py` (líneas 39-53) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` de [PolizaDocumento](../../models/PolizaDocumento.md): Póliza (`polizawidget`,
Select2), descripción y archivo. Sin `clean()` propio: la validación de PDF y tamaño está
en el `FileValidator` del campo del modelo.

## Firma

```python
class PolizaDocumentoForm(forms.ModelForm):
```

## Uso real

`CrearPolizaDocumento`/`UpdatePolizaDocumento` (`carga/views/documentosdigitalesviews.py`).

## Ver también

- [PolizaDocumento](../../models/PolizaDocumento.md)
- [CrearPolizaDocumento](../../views/documentosdigitalesviews/CrearPolizaDocumento.md)
