---
symbol: InstrumentosLegalesMemorandumForm
kind: class
module: secretariador/forms/instrumentoslegalesform.py
lines: 10-54
signature_hash: sha1:f89e642e0921abc05035b644b08d3fe49810390f
authored: true
---

# InstrumentosLegalesMemorandumForm

**Módulo:** `secretariador/forms/instrumentoslegalesform.py` (líneas 10-54) · hereda de `BaseFormMixin, forms.ModelForm`

## Propósito

`ModelForm` para Memorandum. `__init__` precarga `instrumentolegalmemorandum_tipo="P"` (Presidencia) y el año actual como valores iniciales — reduce tipeo para el caso más común sin forzar el valor (el usuario puede cambiarlo).

## Firma

```python
class InstrumentosLegalesMemorandumForm(BaseFormMixin, forms.ModelForm):
```

## Uso real

`CrearInstrumentoLegalMemorandum`/`UpdateInstrumentoLegalMemorandum`.

## Ver también

- [InstrumentosLegalesMemorandum](../../models/InstrumentosLegalesMemorandum.md)
