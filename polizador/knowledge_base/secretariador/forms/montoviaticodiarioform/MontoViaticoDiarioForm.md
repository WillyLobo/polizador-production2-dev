---
symbol: MontoViaticoDiarioForm
kind: class
module: secretariador/forms/montoviaticodiarioform.py
lines: 5-27
signature_hash: sha1:2de65430719dfd1f2e21f3b639bdf93c62bfda96
authored: true
---

# MontoViaticoDiarioForm

**Módulo:** `secretariador/forms/montoviaticodiarioform.py` (líneas 5-27) · hereda de `BaseFormMixin, forms.ModelForm`

## Propósito

Los ocho campos de estrato de `MontoViaticoDiario`, todos con `TextInput`+`inputmode="numeric"` en vez de `NumberInput` — probablemente para tener más control sobre el formato/validación en el cliente que el que da un `<input type="number">` nativo del navegador.

## Firma

```python
class MontoViaticoDiarioForm(BaseFormMixin, forms.ModelForm):
```

## Uso real

Form base de `MontoViaticoDiarioFormset` (`inlineformset_factory` con `max_num=1` — un Decreto tiene a lo sumo un juego de montos).

## Ver también

- [MontoViaticoDiario](../../models/MontoViaticoDiario.md)
