---
symbol: ContratoMontoFormset
kind: class
module: carga/forms/contratoforms.py
lines: 45-47
signature_hash: sha1:1b2f777989fb30ea703fc3a55c945af8706c90d4
authored: true
---

# ContratoMontoFormset

**Módulo:** `carga/forms/contratoforms.py` (líneas 45-47) · hereda de `forms.models.BaseInlineFormSet`

## Propósito

Formset inline de `ContratoMonto` sobre un Contrato (`can_delete=False` — un monto cargado no se borra desde acá, solo se edita). El `__init__` sobreescrito no hace nada distinto del de la clase base (`super().__init__(*args, **kwargs)` sin más) — vestigial, probablemente un lugar preparado para lógica futura que nunca se agregó.

## Firma

```python
class ContratoMontoFormset(forms.models.BaseInlineFormSet):
```

## Uso real

`formset_name = ContratoMontoFormset` en `CrearContrato`/`UpdateContrato` (`FormsetViewMixin`).

## Ver también

- [ContratoMonto](../../models/ContratoMonto.md)
- [ContratoMontoForm](ContratoMontoForm.md)
