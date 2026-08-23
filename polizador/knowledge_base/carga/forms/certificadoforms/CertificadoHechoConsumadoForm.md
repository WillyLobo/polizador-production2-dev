---
symbol: CertificadoHechoConsumadoForm
kind: class
module: carga/forms/certificadoforms.py
lines: 116-147
signature_hash: sha1:4dc480511bafda219e5652cf7792a7f0437338f3
authored: true
---

# CertificadoHechoConsumadoForm

**Módulo:** `carga/forms/certificadoforms.py` (líneas 116-147) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` especializado para Certificado tipo HECHO_CONSUMADO (sin Foja, certifica contra `certificado_contrato_origen`). Sin `clean()` propio — la validación de que el Contrato de origen sea obligatorio vive en `Certificado.clean()`.

## Firma

```python
class CertificadoHechoConsumadoForm(forms.ModelForm):
```

## Uso real

`CrearCertificadoHechoConsumado` (`carga/views/certificadoviews.py`).

## Ver también

- [Certificado](../../models/Certificado.md)
- [CrearCertificadoHechoConsumado](../../views/certificadoviews/CrearCertificadoHechoConsumado.md)
