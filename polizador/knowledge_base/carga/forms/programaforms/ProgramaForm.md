---
symbol: ProgramaForm
kind: class
module: carga/forms/programaforms.py
lines: 4-14
signature_hash: sha1:ce11be721f760ae3c593ca660a46bffab71cd509
authored: true
---

# ProgramaForm

**Módulo:** `carga/forms/programaforms.py` (líneas 4-14) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para Programa, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets` (inputs Bootstrap, sin validación más allá de la del modelo). Un solo campo: `programa_nombre`.

## Firma

```python
class ProgramaForm(forms.ModelForm):
```

## Uso real

`CrearPrograma/UpdatePrograma` (`carga/views/`), tanto para alta como edición.

## Ver también

- [Programa](../../models/Programa.md)
