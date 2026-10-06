---
symbol: delete_region
kind: function
module: api/views/carga_views.py
lines: 431-433
signature_hash: sha1:d4ffb8d6d3eb31ef632697f61101d666ef2fee71
authored: true
---

# delete_region

**Módulo:** `api/views/carga_views.py` (líneas 431-433)

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
