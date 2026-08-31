---
symbol: delete_comisionado
kind: function
module: api/views/secretariador_views.py
lines: 492-494
signature_hash: sha1:03b836d9d94efdc51d51c8a7ed61c7e2dc7fe140
authored: true
---
# delete_comisionado

**Módulo:** `api/views/secretariador_views.py` (líneas 492-494)

## Propósito

Borrado físico (no soft-delete) de un `Agente` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_comisionado(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Agente](../../../secretariador/models/Agente.md)