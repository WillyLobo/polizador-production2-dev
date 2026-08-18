---
symbol: CustomClearableFileInput
kind: class
module: carga/forms/certificadoforms.py
lines: 7-9
signature_hash: sha1:2fed685fb8b638784de57fc3f781eab00c2dfa2d
authored: true
---

# CustomClearableFileInput

**Módulo:** `carga/forms/certificadoforms.py` (líneas 7-9) · hereda de `forms.widgets.ClearableFileInput`

## Propósito

Subclase vacía de `forms.widgets.ClearableFileInput` — el `template_name` custom está comentado (`# template_name = "clearable_file_input.html"`), así que hoy es idéntico al widget base de Django. Probablemente un punto de extensión dejado a medio hacer (para personalizar el render del input de archivo) que nunca se completó.

## Firma

```python
class CustomClearableFileInput(forms.widgets.ClearableFileInput):
```

## Uso real

`certificado_digital` en `CertificadoForm`/`CertificadoAnticipoForm`/`CertificadoHechoConsumadoForm`.

## Ver también

- [CertificadoForm](CertificadoForm.md)
