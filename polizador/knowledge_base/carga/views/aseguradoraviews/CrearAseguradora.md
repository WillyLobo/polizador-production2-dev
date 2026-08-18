---
symbol: CrearAseguradora
kind: class
module: carga/views/aseguradoraviews.py
lines: 21-38
signature_hash: sha1:cd90f5005cd4cdc4bc94b680272c95a8f7089b5e
authored: true
---

# CrearAseguradora

**Módulo:** `carga/views/aseguradoraviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de Aseguradora vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`, `carga/views/ajaxviews.py`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir a otra página.

## Firma

```python
class CrearAseguradora(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearAseguradora` (`carga:crear-aseguradora`).

## Ver también

- [Aseguradora](../../models/Aseguradora.md)
