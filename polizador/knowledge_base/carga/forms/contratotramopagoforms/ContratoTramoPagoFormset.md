---
symbol: ContratoTramoPagoFormset
kind: class
module: carga/forms/contratotramopagoforms.py
lines: 19-43
signature_hash: sha1:25d52d72f3b3ef0c038320a0af31efc091aca8b8
authored: true
---

# ContratoTramoPagoFormset

**Módulo:** `carga/forms/contratotramopagoforms.py` (líneas 19-43) · hereda de `forms.models.BaseInlineFormSet`

## Propósito

Formset inline de `ContratoTramoPago`, con la única validación real de negocio de este
módulo de forms a nivel de conjunto: la suma de `tramo_pct_pago` de todos los tramos (no
borrados) debe dar 100% (con tolerancia de 0.5), y los `tramo_pct_disparador` deben ser
no-decrecientes entre tramos — un tramo posterior no puede dispararse con un % de avance
menor al del tramo anterior, o el orden de certificación no tendría sentido.

## Firma

```python
class ContratoTramoPagoFormset(forms.models.BaseInlineFormSet):
```

## Uso real

`formset_name = ContratoTramoPagoFormset` en `GestionarTramosContrato` (`carga/views/contratotramopagoviews.py`).

## Ver también

- [ContratoTramoPago](../../models/ContratoTramoPago.md)
- [GestionarTramosContrato](../../views/contratotramopagoviews/GestionarTramosContrato.md)
