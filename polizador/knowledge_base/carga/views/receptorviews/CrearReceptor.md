---
symbol: CrearReceptor
kind: class
module: carga/views/receptorviews.py
lines: 20-37
signature_hash: sha1:956d82bddaa64d6915a427be37ab6b8bd67088dd
authored: true
---

# CrearReceptor

**Módulo:** `carga/views/receptorviews.py` (líneas 20-37) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de Receptor vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`, `carga/views/ajaxviews.py`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir a otra página.

## Firma

```python
class CrearReceptor(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearReceptor` (`carga:crear-receptor`).

## Ver también

- [Receptor](../../models/Receptor.md)
