---
symbol: delete_area
kind: function
module: api/views/carga_views.py
lines: 152-154
signature_hash: sha1:6afa05f16d1beeb9889ce2fb9ed130797f28e86a
authored: true
---

# delete_area

**Módulo:** `api/views/carga_views.py` (líneas 152-154)

## Propósito

Borrado físico (no soft-delete) de un `Area` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_area(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Area](../../../carga/models/Area.md)
