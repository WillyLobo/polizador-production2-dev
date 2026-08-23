---
symbol: GeneroAgenteForm
kind: class
module: personalizador/forms/generoagenteforms.py
lines: 4-14
signature_hash: sha1:6130868eb07c802862f015e721bfac88b40c792c
authored: true
---

# GeneroAgenteForm

**Módulo:** `personalizador/forms/generoagenteforms.py` (líneas 4-14) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para GeneroAgente, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets`. Un solo campo: `generoagente_nombre`.

## Firma

```python
class GeneroAgenteForm(forms.ModelForm):
```

## Uso real

`CrearGeneroAgente/UpdateGeneroAgente` (`personalizador/views/`), tanto para alta como edición.

## Ver también

- [GeneroAgente](../../models/GeneroAgente.md)
