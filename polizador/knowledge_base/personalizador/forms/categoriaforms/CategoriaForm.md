---
symbol: CategoriaForm
kind: class
module: personalizador/forms/categoriaforms.py
lines: 4-16
signature_hash: sha1:64b2ef15e7e2496a156d6912c694d48d0b46a6f6
authored: true
---

# CategoriaForm

**Módulo:** `personalizador/forms/categoriaforms.py` (líneas 4-16) · hereda de `forms.ModelForm`

## Propósito

`ModelForm` estándar para Categoria, sin `clean()` ni lógica propia — solo declara `Meta.fields`/`widgets`. Código + nombre.

## Firma

```python
class CategoriaForm(forms.ModelForm):
```

## Uso real

`CrearCategoria/UpdateCategoria` (`personalizador/views/`), tanto para alta como edición.

## Ver también

- [Categoria](../../models/Categoria.md)
