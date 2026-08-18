---
symbol: delete_monto_viatico
kind: function
module: api/views/secretariador_views.py
lines: 454-456
signature_hash: sha1:0a762fa43ddbb8aaa03c72dc5496de0bb50b30d7
authored: true
---

# delete_monto_viatico

**Módulo:** `api/views/secretariador_views.py` (líneas 454-456)

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
