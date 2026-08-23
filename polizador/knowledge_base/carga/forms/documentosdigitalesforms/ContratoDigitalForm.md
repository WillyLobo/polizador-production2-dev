---
symbol: ContratoDigitalForm
kind: class
module: carga/forms/documentosdigitalesforms.py
lines: 5-21
signature_hash: sha1:556c74f169913753a4258f62d7ffee488b920e09
authored: true
---

# ContratoDigitalForm

**Módulo:** `carga/forms/documentosdigitalesforms.py` (líneas 5-21) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para `ContratosDigitales` (documento PDF adjunto a un Contrato, con su `ContratoRubro`/tipo).

## Firma

```python
class ContratoDigitalForm(forms.ModelForm):
```

## Uso real

`CrearContratoDigital`/`UpdateContratoDigital` (`carga/views/documentosdigitalesviews.py`).

## Ver también

- [ContratosDigitales](../../models/ContratosDigitales.md)
