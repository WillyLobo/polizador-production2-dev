---
symbol: ObraDocumentoForm
kind: class
module: carga/forms/documentosdigitalesforms.py
lines: 23-37
signature_hash: sha1:984737aefa811deda0c974e8dc6b56c117d0c91f
authored: true
---

# ObraDocumentoForm

**Módulo:** `carga/forms/documentosdigitalesforms.py` (líneas 23-37) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para `ObraDocumento` (documento PDF adjunto a una Obra, sin tipo/categoría).

## Firma

```python
class ObraDocumentoForm(forms.ModelForm):
```

## Uso real

`CrearObraDocumento`/`UpdateObraDocumento` (`carga/views/documentosdigitalesviews.py`).

## Ver también

- [ObraDocumento](../../models/ObraDocumento.md)
