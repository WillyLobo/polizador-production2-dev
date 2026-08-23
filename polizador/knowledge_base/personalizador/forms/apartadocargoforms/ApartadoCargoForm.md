---
symbol: ApartadoCargoForm
kind: class
module: personalizador/forms/apartadocargoforms.py
lines: 4-14
signature_hash: sha1:da4df9dcdb341790cb9446cd27d70f575f1b97d2
authored: true
---

# ApartadoCargoForm

**Módulo:** `personalizador/forms/apartadocargoforms.py` (líneas 4-14) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para ApartadoCargo, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets`. Un solo campo: `apartadocargo_denominacion`.

## Firma

```python
class ApartadoCargoForm(forms.ModelForm):
```

## Uso real

`CrearApartadoCargo/UpdateApartadoCargo` (`personalizador/views/`), tanto para alta como edición.

## Ver también

- [ApartadoCargo](../../models/ApartadoCargo.md)
