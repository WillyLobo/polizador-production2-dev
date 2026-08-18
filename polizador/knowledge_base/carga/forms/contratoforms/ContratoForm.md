---
symbol: ContratoForm
kind: class
module: carga/forms/contratoforms.py
lines: 9-44
signature_hash: sha1:ccb506e78e86295b5ea478b0dabd4ee769856429
authored: true
---

# ContratoForm

**Módulo:** `carga/forms/contratoforms.py` (líneas 9-44) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para Contrato: datos de resolución + el flag `contrato_certificacion_por_etapas` que decide si la Obra certifica por % mensual o por tramos fijos (ver la página del modelo). Sin `clean()` propio; el único `__init__` custom solo fuerza un label ("Obra") en un campo que no lo trae por defecto.

## Firma

```python
class ContratoForm(forms.ModelForm):
```

## Uso real

`CrearContrato`/`UpdateContrato` (`carga/views/contratoviews.py`).

## Ver también

- [Contrato](../../models/Contrato.md)
