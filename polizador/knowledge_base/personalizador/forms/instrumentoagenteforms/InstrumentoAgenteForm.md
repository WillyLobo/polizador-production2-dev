---
symbol: InstrumentoAgenteForm
kind: class
module: personalizador/forms/instrumentoagenteforms.py
lines: 5-25
signature_hash: sha1:e1230ba02b0d60d06ffebaa3d5ad7954cbbede81
authored: false
---

# InstrumentoAgenteForm

**Módulo:** `personalizador/forms/instrumentoagenteforms.py` (líneas 5-25)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class InstrumentoAgenteForm(forms.ModelForm):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `personalizador/views/instrumentoagenteviews.py:27` — `form_class = InstrumentoAgenteForm`
- `personalizador/views/instrumentoagenteviews.py:51` — `form_class = InstrumentoAgenteForm`
- `personalizador/forms/instrumentoagenteforms.py:27` — `class InstrumentoAgentePopupForm(InstrumentoAgenteForm):`
- `personalizador/forms/instrumentoagenteforms.py:31` — `class Meta(InstrumentoAgenteForm.Meta):`
- `personalizador/forms/instrumentoagenteforms.py:32` — `fields = tuple(f for f in InstrumentoAgenteForm.Meta.fields if f != "instrumentoagente")`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
