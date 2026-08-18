---
symbol: UpdateSolicitudExterior
kind: class
module: secretariador/views/solicitud_exteriorviews.py
lines: 227-279
signature_hash: sha1:2a7175a8a6a7e55bf0f4333735aec635eb2dafdc
authored: true
---

# UpdateSolicitudExterior

**Módulo:** `secretariador/views/solicitud_exteriorviews.py` (líneas 227-279) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de Solicitud Exterior, mismo patrón get/post manual que `CrearSolicitudExterior`.

## Firma

```python
class UpdateSolicitudExterior(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdateSolicitudExterior` (`secretariador:update-solicitud-exterior`).

## Ver también

- [Solicitud](../../models/Solicitud.md)
