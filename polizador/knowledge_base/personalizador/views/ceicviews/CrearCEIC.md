---
symbol: CrearCEIC
kind: class
module: personalizador/views/ceicviews.py
lines: 21-38
signature_hash: sha1:046692ce5d8f97aaf3d8170aeb1783bc73cda7e1
authored: true
---

# CrearCEIC

**Módulo:** `personalizador/views/ceicviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de CEIC vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir.

## Firma

```python
class CrearCEIC(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearCEIC` (`personalizador:crear-ceic`).

## Ver también

- [CEIC](../../models/CEIC.md)
