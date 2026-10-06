---
symbol: delete_movimiento
kind: function
module: api/views/carga_views.py
lines: 1963-1965
signature_hash: sha1:62bed0378c5025eeb1b29b147d56c1e4f77a5f5b
authored: true
---

# delete_movimiento

**Módulo:** `api/views/carga_views.py` (líneas 1963-1965)

## Propósito

Borrado físico (no soft-delete) de un `Poliza_Movimiento` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_movimiento(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Poliza_Movimiento](../../../carga/models/Poliza_Movimiento.md)
- [Poliza](../../../carga/models/Poliza.md)
