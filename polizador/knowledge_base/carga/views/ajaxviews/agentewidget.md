---
symbol: agentewidget
kind: class
module: carga/views/ajaxviews.py
lines: 145-149
signature_hash: sha1:960ef44604d8612a1c2f1d6405b14eba1b2e9740
authored: true
---

# agentewidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 145-149) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Agente (personalizador) vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Selección simple, mismos `search_fields` que `agentemultiplewidget`.

## Firma

```python
class agentewidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

Campos `ForeignKey` a Agente en formularios de `carga`.

## Ver también

- [agentemultiplewidget](agentemultiplewidget.md)
