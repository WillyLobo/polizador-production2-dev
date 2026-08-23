---
symbol: polizawidget
kind: class
module: carga/views/ajaxviews.py
lines: 169-176
signature_hash: sha1:b065903523c4b8f218fbf005ab3216b531a140cf
authored: true
---

# polizawidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 169-176) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Poliza vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Busca por número, expediente, aseguradora, tomador y Obra.

## Firma

```python
class polizawidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

Campos `ForeignKey` a Poliza (ej. `Poliza_Movimiento.poliza_movimiento_numero`).

## Ver también

- [Poliza](../../models/Poliza.md)
