---
symbol: VerSolicitud
kind: class
module: secretariador/views/solicitudviews.py
lines: 192-196
signature_hash: sha1:5acb9af5412f10ab9ba38d3e2a0902eb028d2e82
authored: true
---

# VerSolicitud

**Módulo:** `secretariador/views/solicitudviews.py` (líneas 192-196) · hereda de `PermissionRequiredMixin, generic.DetailView`

## Propósito

Ficha de detalle de una Solicitud (sin lógica propia más allá del `DetailView`).

## Firma

```python
class VerSolicitud(PermissionRequiredMixin, generic.DetailView):
```

## Uso real

`VerSolicitud` (`secretariador:ver-solicitud`).

## Ver también

- [Solicitud](../../models/Solicitud.md)
