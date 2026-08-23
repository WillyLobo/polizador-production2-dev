---
symbol: ContratoMontoForm
kind: class
module: carga/forms/contratomontoforms.py
lines: 5-24
signature_hash: sha1:b01510f234d1e845f0ce450f381c2bff5f39813f
authored: true
---

# ContratoMontoForm

**Módulo:** `carga/forms/contratomontoforms.py` (líneas 5-24) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para ContratoMonto (monto por rubro+financiamiento de un Contrato). Sin lógica propia.

## Firma

```python
class ContratoMontoForm(forms.ModelForm):
```

## Uso real

Form base de `ContratoMontoFormset` (`carga/forms/contratoforms.py`).

## Ver también

- [ContratoMonto](../../models/ContratoMonto.md)
- [ContratoMontoFormset](ContratoMontoFormset.md)
