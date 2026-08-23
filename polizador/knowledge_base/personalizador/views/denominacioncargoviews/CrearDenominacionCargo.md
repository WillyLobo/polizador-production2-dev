---
symbol: CrearDenominacionCargo
kind: class
module: personalizador/views/denominacioncargoviews.py
lines: 21-38
signature_hash: sha1:862546d8d8d8fe0b55e5cf767fd1b530cca4d3bf
authored: true
---

# CrearDenominacionCargo

**Módulo:** `personalizador/views/denominacioncargoviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de DenominacionCargo vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir.

## Firma

```python
class CrearDenominacionCargo(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearDenominacionCargo` (`personalizador:crear-denominacioncargo`).

## Ver también

- [DenominacionCargo](../../models/DenominacionCargo.md)
