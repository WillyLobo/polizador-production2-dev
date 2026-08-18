---
symbol: CEICForm
kind: class
module: personalizador/forms/ceicforms.py
lines: 4-14
signature_hash: sha1:8fbf697d0a9445fe1a2ff3065de661a0d514adbb
authored: true
---

# CEICForm

**Módulo:** `personalizador/forms/ceicforms.py` (líneas 4-14) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para CEIC, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets`. Un solo campo: `ceic`.

## Firma

```python
class CEICForm(forms.ModelForm):
```

## Uso real

`CrearCEIC/UpdateCEIC` (`personalizador/views/`), tanto para alta como edición.

## Ver también

- [CEIC](../../models/CEIC.md)
