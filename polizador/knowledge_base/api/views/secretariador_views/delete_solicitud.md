---
symbol: delete_solicitud
kind: function
module: api/views/secretariador_views.py
lines: 620-622
signature_hash: sha1:4777f909f89eed09c1fe4e499881e31ce94a5903
authored: true
---
# delete_solicitud

**Módulo:** `api/views/secretariador_views.py` (líneas 620-622)

## Propósito

Borrado físico (no soft-delete) de un `Solicitud` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_solicitud(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Solicitud](../../../secretariador/models/Solicitud.md)