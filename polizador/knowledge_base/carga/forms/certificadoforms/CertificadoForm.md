---
symbol: CertificadoForm
kind: class
module: carga/forms/certificadoforms.py
lines: 11-61
signature_hash: sha1:cb16a473f5b8cb7d0de1e2fa6fff5c64a7b2fa53
authored: true
---

# CertificadoForm

**Módulo:** `carga/forms/certificadoforms.py` (líneas 11-61) · hereda de `forms.ModelForm`

## Propósito

El `ModelForm` "genérico" de Certificado (sin tipo forzado — a diferencia de `CertificadoAnticipoForm`/`CertificadoHechoConsumadoForm`), usado tanto para alta manual como para edición. `certificado_foja` es `HiddenInput` — se precarga por querystring en `CrearCertificado.get_initial`, no se elige desde este form. Sin `clean()` propio: toda la validación cruzada por tipo vive en `Certificado.clean()` (modelo), que corre igual sobre esta instancia.

## Firma

```python
class CertificadoForm(forms.ModelForm):
```

## Uso real

`CrearCertificado`/`UpdateCertificado` (`carga/views/certificadoviews.py`).

## Ver también

- [Certificado](../../models/Certificado.md)
- [CrearCertificado](../../views/certificadoviews/CrearCertificado.md)
