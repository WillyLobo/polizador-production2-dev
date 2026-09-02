---
symbol: InstrumentosLegalesResolucionesDirectorioForm
kind: class
module: secretariador/forms/instrumentoslegalesform.py
lines: 164-216
signature_hash: sha1:58aaf9683ac4d892879b79ea278c1bef5007140f
authored: true
---
# InstrumentosLegalesResolucionesDirectorioForm

**Módulo:** `secretariador/forms/instrumentoslegalesform.py` (líneas 164-216) · hereda de `BaseFormMixin, forms.ModelForm`

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