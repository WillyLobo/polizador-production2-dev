---
symbol: delete_monto_viatico
kind: function
module: api/views/secretariador_views.py
lines: 461-463
signature_hash: sha1:e25cb3b6e4b9174b1dd4e1992ccc238262b3e303
authored: true
---
# delete_monto_viatico

**Módulo:** `api/views/secretariador_views.py` (líneas 461-463)

## Propósito

Borrado físico (no soft-delete) de un `MontoViaticoDiario` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_monto_viatico(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [MontoViaticoDiario](../../../secretariador/models/MontoViaticoDiario.md)