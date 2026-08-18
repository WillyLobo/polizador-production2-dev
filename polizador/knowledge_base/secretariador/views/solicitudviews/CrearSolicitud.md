---
symbol: CrearSolicitud
kind: class
module: secretariador/views/solicitudviews.py
lines: 157-170
signature_hash: sha1:00ecd67842c5d66975e444cba89dc875c58e91b1
authored: true
---

# CrearSolicitud

**Módulo:** `secretariador/views/solicitudviews.py` (líneas 157-170) · hereda de `PermissionRequiredMixin, UserFormsetKwargsMixin, FormsetViewMixin, generic.CreateView`

## Propósito

Alta de Solicitud junto con su formset inline de `ComisionadoSolicitud` (`FormsetViewMixin` + `UserFormsetKwargsMixin`, para que el formset tenga acceso al usuario logueado).

## Firma

```python
class CrearSolicitud(PermissionRequiredMixin, UserFormsetKwargsMixin, FormsetViewMixin, generic.CreateView):
```

## Uso real

`CrearSolicitud` (`secretariador:crear-solicitud`), enlazada desde el navbar ("Viáticos > Nueva Solicitud", vía `redirect_solicitud`).

## Ver también

- [Solicitud](../../models/Solicitud.md)
- [ComisionadoSolicitud](../../models/ComisionadoSolicitud.md)
