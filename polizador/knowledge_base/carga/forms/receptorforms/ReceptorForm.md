---
symbol: ReceptorForm
kind: class
module: carga/forms/receptorforms.py
lines: 4-14
signature_hash: sha1:48c27da77bc5dea999209ee833785d14cc92897f
authored: true
---

# ReceptorForm

**Módulo:** `carga/forms/receptorforms.py` (líneas 4-14) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para Receptor, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets` (inputs Bootstrap, sin validación más allá de la del modelo). Un solo campo: `receptor_nombre`.

## Firma

```python
class ReceptorForm(forms.ModelForm):
```

## Uso real

`CrearReceptor/UpdateReceptor` (`carga/views/`), tanto para alta como edición.

## Ver también

- [Receptor](../../models/Receptor.md)
