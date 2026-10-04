---
symbol: update_area
kind: function
module: api/views/carga_views.py
lines: 142-147
signature_hash: sha1:c687574807be8dbb3cf00513d7e7dee06039e826
authored: true
---

# update_area

**Módulo:** `api/views/carga_views.py` (líneas 142-147)

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
