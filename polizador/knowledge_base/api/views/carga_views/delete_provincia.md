---
symbol: delete_provincia
kind: function
module: api/views/carga_views.py
lines: 393-395
signature_hash: sha1:d1f8ed42ad54a9443fab53b13844dda45f17713b
authored: true
---

# delete_provincia

**Módulo:** `api/views/carga_views.py` (líneas 393-395)

## Propósito

Borrado físico (no soft-delete) de un `Provincia` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_provincia(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Provincia](../../../carga/models/Provincia.md)
