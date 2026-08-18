---
symbol: update_region
kind: function
module: api/views/carga_views.py
lines: 420-425
signature_hash: sha1:fa4e1e014cb3fecf5aba69f919ed8b5963af4e62
authored: true
---

# update_region

**Módulo:** `api/views/carga_views.py` (líneas 420-425)

## Propósito

Actualización parcial de un `Region` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_region(request, id: int, payload: RegionUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`RegionOut`.

## Ver también

- [Region](../../../carga/models/Region.md)
