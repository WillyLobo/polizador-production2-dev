---
symbol: delete_region
kind: function
module: api/views/carga_views.py
lines: 430-432
signature_hash: sha1:40ec1c0dbcc458c72989df39246e46f191c5b537
authored: true
---

# delete_region

**Módulo:** `api/views/carga_views.py` (líneas 430-432)

## Propósito

Borrado físico (no soft-delete) de un `Region` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_region(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Region](../../../carga/models/Region.md)
