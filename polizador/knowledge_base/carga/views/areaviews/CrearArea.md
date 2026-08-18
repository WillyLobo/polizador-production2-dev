---
symbol: CrearArea
kind: class
module: carga/views/areaviews.py
lines: 11-27
signature_hash: sha1:6212f54211412a540cc277b84ae093be428d0fd0
authored: true
---

# CrearArea

**Módulo:** `carga/views/areaviews.py` (líneas 11-27) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de Area vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`, `carga/views/ajaxviews.py`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir a otra página.

## Firma

```python
class CrearArea(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearArea` (`carga:crear-area`).

## Ver también

- [Area](../../models/Area.md)
