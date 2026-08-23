---
symbol: InstrumentosLegalesResolucionesPresidenciaForm
kind: class
module: secretariador/forms/instrumentoslegalesform.py
lines: 95-139
signature_hash: sha1:7b4b757b1c030072b18b347958386ff992a8f675
authored: true
---

# InstrumentosLegalesResolucionesPresidenciaForm

**Módulo:** `secretariador/forms/instrumentoslegalesform.py` (líneas 95-139) · hereda de `BaseFormMixin, forms.ModelForm`

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
