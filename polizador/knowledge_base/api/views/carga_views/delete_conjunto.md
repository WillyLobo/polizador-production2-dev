---
symbol: delete_conjunto
kind: function
module: api/views/carga_views.py
lines: 1503-1505
signature_hash: sha1:a0a35718b0f462e38c622b834f88e67b30ecaa75
authored: true
---

# delete_conjunto

**Módulo:** `api/views/carga_views.py` (líneas 1503-1505)

## Propósito

Borrado físico (no soft-delete) de un `ConjuntoLicitado` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_conjunto(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [ConjuntoLicitado](../../../carga/models/ConjuntoLicitado.md)
