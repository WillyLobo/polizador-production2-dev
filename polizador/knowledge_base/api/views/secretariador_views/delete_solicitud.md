---
symbol: delete_solicitud
kind: function
module: api/views/secretariador_views.py
lines: 613-615
signature_hash: sha1:57a0846453805764f488eae2523dd706f5fc5d22
authored: true
---

# delete_solicitud

**Módulo:** `api/views/secretariador_views.py` (líneas 613-615)

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
