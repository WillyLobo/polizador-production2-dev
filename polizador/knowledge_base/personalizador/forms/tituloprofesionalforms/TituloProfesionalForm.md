---
symbol: TituloProfesionalForm
kind: class
module: personalizador/forms/tituloprofesionalforms.py
lines: 4-18
signature_hash: sha1:0e318d195b4db7e7c7e78c18afceb2b1d3c2f5dd
authored: true
---

# TituloProfesionalForm

**Módulo:** `personalizador/forms/tituloprofesionalforms.py` (líneas 4-18) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para TituloProfesional, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets`. Nombre + abreviatura + grado académico.

## Firma

```python
class TituloProfesionalForm(forms.ModelForm):
```

## Uso real

`CrearTituloProfesional/UpdateTituloProfesional` (`personalizador/views/`), tanto para alta como edición.

## Ver también

- [TituloProfesional](../../models/TituloProfesional.md)
