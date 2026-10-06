---
symbol: update_region
kind: function
module: api/views/carga_views.py
lines: 421-426
signature_hash: sha1:04d26e6b5788d81bed6166f10001127faa997517
authored: true
---

# update_region

**Módulo:** `api/views/carga_views.py` (líneas 421-426)

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
