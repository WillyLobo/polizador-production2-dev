---
symbol: EncabezadoDocumentoForm
kind: class
module: secretariador/forms/encabezadoform.py
lines: 8-27
signature_hash: sha1:83c277ecbe6c77dfb71d127d55c28fd0b3f9563b
authored: true
---

# EncabezadoDocumentoForm

**Módulo:** `secretariador/forms/encabezadoform.py` (líneas 8-27) · hereda de `BaseFormMixin, forms.ModelForm`

## Propósito

`ModelForm` para subir un `EncabezadoDocumento`. Su único campo tiene un `clean_encabezadodocumento_archivo` propio: delega en `secretariador.docx_header.tiene_encabezado_valido(archivo)` (fuera del alcance de este manifest) para rechazar un `.docx` que no tenga un encabezado de primera página reconocible — evita subir un archivo que rompería silenciosamente la generación de documentos más adelante.

## Firma

```python
class EncabezadoDocumentoForm(BaseFormMixin, forms.ModelForm):
```

## Uso real

`ActualizarEncabezado` (`secretariador/views/encabezadoviews.py`).

## Ver también

- [EncabezadoDocumento](../../models/EncabezadoDocumento.md)
