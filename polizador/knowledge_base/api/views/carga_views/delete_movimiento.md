---
symbol: delete_movimiento
kind: function
module: api/views/carga_views.py
lines: 1942-1944
signature_hash: sha1:ca270a50f5efec6c6c5ec1d34edef20252088063
authored: true
---

# delete_movimiento

**Módulo:** `api/views/carga_views.py` (líneas 1942-1944)

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
