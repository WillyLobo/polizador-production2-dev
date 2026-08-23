---
symbol: delete_area
kind: function
module: api/views/carga_views.py
lines: 151-153
signature_hash: sha1:eab8a92ec60d432439127e43dd360b034812ff74
authored: true
---

# delete_area

**Módulo:** `api/views/carga_views.py` (líneas 151-153)

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
