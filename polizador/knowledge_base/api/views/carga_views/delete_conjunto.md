---
symbol: delete_conjunto
kind: function
module: api/views/carga_views.py
lines: 1502-1504
signature_hash: sha1:12dfffc880096a7a0c87f674c062a7bd0b2d4c70
authored: true
---

# delete_conjunto

**Módulo:** `api/views/carga_views.py` (líneas 1502-1504)

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
