---
symbol: agentemultiplewidget
kind: class
module: carga/views/ajaxviews.py
lines: 139-143
signature_hash: sha1:289068b8457546fa20596d9360765661c23eb3c5
authored: true
---

# agentemultiplewidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 139-143) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Agente (personalizador) vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Selección múltiple (`ModelSelect2MultipleWidget`), busca por nombres y apellidos.

## Firma

```python
class agentemultiplewidget(LoginRequiredMixin, s2forms.ModelSelect2MultipleWidget):
```

## Uso real

`Obra.obra_inspector`, `FojaDeMedicion.foja_inspector` (ambos `ManyToManyField`).

## Ver también

- [Obra](../../models/Obra.md)
- [FojaDeMedicion](../../models/FojaDeMedicion.md)
