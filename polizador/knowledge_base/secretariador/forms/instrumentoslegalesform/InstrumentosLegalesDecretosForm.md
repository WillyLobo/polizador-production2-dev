---
symbol: InstrumentosLegalesDecretosForm
kind: class
module: secretariador/forms/instrumentoslegalesform.py
lines: 56-108
signature_hash: sha1:b56786e842c382848e615edacb983c391b38d7e5
authored: true
---
# InstrumentosLegalesDecretosForm

**Módulo:** `secretariador/forms/instrumentoslegalesform.py` (líneas 56-108) · hereda de `BaseFormMixin, forms.ModelForm`

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