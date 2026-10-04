---
symbol: update_conjunto
kind: function
module: api/views/carga_views.py
lines: 1493-1498
signature_hash: sha1:33fc999b0cd69ab9a6156e3d20fdb622d8c1954d
authored: true
---

# update_conjunto

**Módulo:** `api/views/carga_views.py` (líneas 1493-1498)

## Propósito

Actualización parcial de un `ConjuntoLicitado` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_conjunto(request, id: int, payload: ConjuntoLicitadoUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`ConjuntoLicitadoOut`.

## Ver también

- [ConjuntoLicitado](../../../carga/models/ConjuntoLicitado.md)
