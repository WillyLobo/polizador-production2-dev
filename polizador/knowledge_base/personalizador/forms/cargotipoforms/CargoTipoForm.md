---
symbol: CargoTipoForm
kind: class
module: personalizador/forms/cargotipoforms.py
lines: 4-14
signature_hash: sha1:fdf740bcf94ad8aac2d6e7412643f3a15d4e67a1
authored: true
---

# CargoTipoForm

**Módulo:** `personalizador/forms/cargotipoforms.py` (líneas 4-14) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para CargoTipo, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets`. Un solo campo: `cargotipo`.

## Firma

```python
class CargoTipoForm(forms.ModelForm):
```

## Uso real

`CrearCargoTipo/UpdateCargoTipo` (`personalizador/views/`), tanto para alta como edición.

## Ver también

- [CargoTipo](../../models/CargoTipo.md)
