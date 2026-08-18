---
symbol: UpdateSolicitud
kind: class
module: secretariador/views/solicitudviews.py
lines: 173-181
signature_hash: sha1:7fea5b8aa9f08275f48182ef828e453012770e13
authored: true
---

# UpdateSolicitud

**Módulo:** `secretariador/views/solicitudviews.py` (líneas 173-181) · hereda de `PermissionRequiredMixin, UserFormsetKwargsMixin, FormsetViewMixin, generic.UpdateView`

## Propósito

Edición de Solicitud + formset de comisionados.

## Firma

```python
class UpdateSolicitud(PermissionRequiredMixin, UserFormsetKwargsMixin, FormsetViewMixin, generic.UpdateView):
```

## Uso real

`UpdateSolicitud` (`secretariador:update-solicitud`).

## Ver también

- [Solicitud](../../models/Solicitud.md)
