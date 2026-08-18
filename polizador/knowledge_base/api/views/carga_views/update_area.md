---
symbol: update_area
kind: function
module: api/views/carga_views.py
lines: 141-146
signature_hash: sha1:cd64b43b0d3090b5e1342e7708ca4d167f7710dc
authored: true
---

# update_area

**Módulo:** `api/views/carga_views.py` (líneas 141-146)

## Propósito

Actualización parcial de un `Area` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_area(request, id: int, payload: AreaUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`AreaOut`.

## Ver también

- [Area](../../../carga/models/Area.md)
