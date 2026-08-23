---
symbol: CertificadoAnticipoForm
kind: class
module: carga/forms/certificadoforms.py
lines: 77-114
signature_hash: sha1:c3f0877de4698ff0a18ff7798b3c809d6b2c3d57
authored: true
---

# CertificadoAnticipoForm

**Módulo:** `carga/forms/certificadoforms.py` (líneas 77-114) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` especializado para Certificado tipo ANTICIPO (sin Foja, con `certificado_anticipo_pct` cargado a mano). `clean()` delega en `certificacion.validar_anticipo_nuevo(obra, financiamiento, pct)` la regla de negocio real (probablemente: que el % acumulado de anticipos no exceda algún límite) y traduce su `ValidationError` a un error de formulario.

## Firma

```python
class CertificadoAnticipoForm(forms.ModelForm):
```

## Uso real

`CrearCertificadoAnticipo` (`carga/views/certificadoviews.py`).

## Ver también

- [Certificado](../../models/Certificado.md)
- [CrearCertificadoAnticipo](../../views/certificadoviews/CrearCertificadoAnticipo.md)
