---
symbol: CorteLicenciaForm
kind: class
module: personalizador/forms/cortelicenciaforms.py
lines: 6-33
signature_hash: sha1:31cdb329bd7d20c6a2e345a14861ed9a62b929c5
authored: true
---

# CorteLicenciaForm

**Módulo:** `personalizador/forms/cortelicenciaforms.py` (líneas 6-33) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` para `CorteLicencia`: `cortelicencia_licencia` es `HiddenInput` (se precarga en la vista desde la URL, `licenciapermiso_pk` — el usuario nunca la elige desde este form). Sin `clean()` propio: la validación cruzada (tipo de licencia válido para corte, fechas dentro de rango, días que no superen el total) vive en `CorteLicencia.clean()`.

## Firma

```python
class CorteLicenciaForm(forms.ModelForm):
```

## Uso real

`CrearCorteLicencia`/`UpdateCorteLicencia` (`personalizador/views/cortelicenciaviews.py`).

## Ver también

- [CorteLicencia](../../models/CorteLicencia.md)
