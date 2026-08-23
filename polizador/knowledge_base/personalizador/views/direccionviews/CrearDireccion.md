---
symbol: CrearDireccion
kind: class
module: personalizador/views/direccionviews.py
lines: 21-38
signature_hash: sha1:71f2c9c04dbc96743f73221485b13f8eff95c2b9
authored: true
---

# CrearDireccion

**Módulo:** `personalizador/views/direccionviews.py` (líneas 21-38) · hereda de `PopupCreateMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de Direccion vía `ModelForm` estándar. Usa `PopupCreateMixin` (`core/mixins.py`): si se abre en el modal de "agregar relacionado" de un widget select2 (`AddRelatedWidgetMixin`), devuelve el objeto creado como opción ya seleccionada en vez de redirigir.

## Firma

```python
class CrearDireccion(PopupCreateMixin, PermissionRequiredMixin, generic.CreateView):
```

## Uso real

`CrearDireccion` (`personalizador:crear-direccion`).

## Ver también

- [Direccion](../../models/Direccion.md)
