---
symbol: delete_comisionado_solicitud
kind: function
module: api/views/secretariador_views.py
lines: 818-820
signature_hash: sha1:eff607f1f6541227fcb3fbf409b2b00255a1bef0
authored: true
---
# delete_comisionado_solicitud

**Módulo:** `api/views/secretariador_views.py` (líneas 818-820)

## Propósito

Borrado físico (no soft-delete) de un `ComisionadoSolicitud` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_comisionado_solicitud(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [ComisionadoSolicitud](../../../secretariador/models/ComisionadoSolicitud.md)