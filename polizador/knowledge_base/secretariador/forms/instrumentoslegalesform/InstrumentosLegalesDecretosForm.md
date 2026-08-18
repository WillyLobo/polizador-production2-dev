---
symbol: InstrumentosLegalesDecretosForm
kind: class
module: secretariador/forms/instrumentoslegalesform.py
lines: 56-93
signature_hash: sha1:50b6b5289aaf99f51d2d65d10341513e50c4b587
authored: true
---

# InstrumentosLegalesDecretosForm

**Módulo:** `secretariador/forms/instrumentoslegalesform.py` (líneas 56-93) · hereda de `BaseFormMixin, forms.ModelForm`

## Propósito

`ModelForm` para Decreto. Mismo patrón de `__init__` con tipo/año por defecto que `InstrumentosLegalesMemorandumForm`.

## Firma

```python
class InstrumentosLegalesDecretosForm(BaseFormMixin, forms.ModelForm):
```

## Uso real

`CrearInstrumentoLegalDecreto`/`UpdateInstrumentoLegalDecreto`, y reusado en `CrearMontoViaticoDiario`/`UpdateMontoViaticoDiario` (el form del Decreto, con el formset de montos aparte).

## Ver también

- [InstrumentosLegalesDecretos](../../models/InstrumentosLegalesDecretos.md)
