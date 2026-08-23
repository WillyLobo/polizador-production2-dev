---
symbol: GenerarCertificadosDesdeFojaForm
kind: class
module: carga/forms/certificadoforms.py
lines: 63-75
signature_hash: sha1:7dfa6460cd7d14c3c25adee16840e877bc633d33
authored: true
---

# GenerarCertificadosDesdeFojaForm

**Módulo:** `carga/forms/certificadoforms.py` (líneas 63-75) · hereda de `forms.Form`

## Propósito

`forms.Form` simple (no `ModelForm` — no hay una instancia de Certificado todavía en este paso): solo pide expediente y fecha, los datos de actuación que se van a aplicar a todos los certificados que se generen desde la Foja.

## Firma

```python
class GenerarCertificadosDesdeFojaForm(forms.Form):
```

## Uso real

`GenerarCertificadosDesdeFoja` (`carga/views/certificadoviews.py`).

## Ver también

- [GenerarCertificadosDesdeFoja](../../views/certificadoviews/GenerarCertificadosDesdeFoja.md)
