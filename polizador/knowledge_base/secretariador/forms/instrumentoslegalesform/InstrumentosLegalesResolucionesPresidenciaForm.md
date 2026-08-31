---
symbol: InstrumentosLegalesResolucionesPresidenciaForm
kind: class
module: secretariador/forms/instrumentoslegalesform.py
lines: 110-162
signature_hash: sha1:4e3632e51b7e2c21e2b778d11ab866aa671f3f79
authored: true
---
# InstrumentosLegalesResolucionesPresidenciaForm

**Módulo:** `secretariador/forms/instrumentoslegalesform.py` (líneas 110-162) · hereda de `BaseFormMixin, forms.ModelForm`

## Propósito

`ModelForm` para Resolución de Presidencia — sin campo `instrumentolegalresoluciones_acta` (solo aplica a Directorio). `__init__` precarga `tipo="P"` y el año actual.

## Firma

```python
class InstrumentosLegalesResolucionesPresidenciaForm(BaseFormMixin, forms.ModelForm):
```

## Uso real

`CrearInstrumentoLegalResolucionPresidencia`/`UpdateInstrumentoLegalResolucionPresidencia`.

## Ver también

- [InstrumentosLegalesResoluciones](../../models/InstrumentosLegalesResoluciones.md)
- [InstrumentosLegalesResolucionesDirectorioForm](InstrumentosLegalesResolucionesDirectorioForm.md)