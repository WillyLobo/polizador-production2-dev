---
symbol: DenominacionCargoForm
kind: class
module: personalizador/forms/denominacioncargoforms.py
lines: 4-14
signature_hash: sha1:edb83ff1966576d6d51e5f6fb7840c8bb8fe368c
authored: true
---

# DenominacionCargoForm

**Módulo:** `personalizador/forms/denominacioncargoforms.py` (líneas 4-14) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para DenominacionCargo, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets`. Un solo campo: `denominacion`.

## Firma

```python
class DenominacionCargoForm(forms.ModelForm):
```

## Uso real

`CrearDenominacionCargo/UpdateDenominacionCargo` (`personalizador/views/`), tanto para alta como edición.

## Ver también

- [DenominacionCargo](../../models/DenominacionCargo.md)
