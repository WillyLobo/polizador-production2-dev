---
symbol: obrawidget
kind: class
module: carga/views/ajaxviews.py
lines: 58-63
signature_hash: sha1:0752e061da799ae6a481b78c440e173d913490e8
authored: true
---

# obrawidget

**Módulo:** `carga/views/ajaxviews.py` (líneas 58-63) · hereda de `LoginRequiredMixin, s2forms.ModelSelect2Widget`

## Propósito

Widget select2 (`django-select2`) para elegir un(a) Obra vía búsqueda AJAX incremental, en vez de un `<select>` con todas las opciones cargadas de una — ver CLAUDE.md sobre `django-select2`. `search_fields` define contra qué columnas busca `django-select2` con `icontains`. Busca por nombre, empresa contratista y convenio/ACU.

## Firma

```python
class obrawidget(LoginRequiredMixin, s2forms.ModelSelect2Widget):
```

## Uso real

Campo `ForeignKey` a Obra en varios forms (`ContratoForm`, `PolizaForm`, `PlanDeTrabajosForm`...).

## Ver también

- [Obra](../../models/Obra.md)
