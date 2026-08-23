---
symbol: InstrumentosLegalesResolucionesDirectorioForm
kind: class
module: secretariador/forms/instrumentoslegalesform.py
lines: 141-189
signature_hash: sha1:84f6243c23778a1bdec7ff65900425f04b1a5206
authored: true
---

# InstrumentosLegalesResolucionesDirectorioForm

**Módulo:** `secretariador/forms/instrumentoslegalesform.py` (líneas 141-189) · hereda de `BaseFormMixin, forms.ModelForm`

## Propósito

Misma base que la variante Presidencia, con `instrumentolegalresoluciones_acta` agregado. `__init__` precarga `tipo="D"` en vez de `"P"`.

## Firma

```python
class InstrumentosLegalesResolucionesDirectorioForm(BaseFormMixin, forms.ModelForm):
```

## Uso real

`CrearInstrumentoLegalResolucionDirectorio`/`UpdateInstrumentoLegalResolucionDirectorio`.

## Ver también

- [InstrumentosLegalesResoluciones](../../models/InstrumentosLegalesResoluciones.md)
- [InstrumentosLegalesResolucionesPresidenciaForm](InstrumentosLegalesResolucionesPresidenciaForm.md)
