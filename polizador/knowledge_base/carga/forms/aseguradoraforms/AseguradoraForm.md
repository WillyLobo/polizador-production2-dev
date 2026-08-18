---
symbol: AseguradoraForm
kind: class
module: carga/forms/aseguradoraforms.py
lines: 4-14
signature_hash: sha1:5566215ce05325d4db5282bd3fa6a9b1e92a3903
authored: true
---

# AseguradoraForm

**Módulo:** `carga/forms/aseguradoraforms.py` (líneas 4-14) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para Aseguradora, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets` (inputs Bootstrap, sin validación más allá de la del modelo). Un solo campo: `aseguradora_nombre`.

## Firma

```python
class AseguradoraForm(forms.ModelForm):
```

## Uso real

`CrearAseguradora/UpdateAseguradora` (`carga/views/`), tanto para alta como edición.

## Ver también

- [Aseguradora](../../models/Aseguradora.md)
