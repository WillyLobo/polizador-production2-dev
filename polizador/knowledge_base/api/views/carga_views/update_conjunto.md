---
symbol: update_conjunto
kind: function
module: api/views/carga_views.py
lines: 1492-1497
signature_hash: sha1:5d760b44b060fd2177d3a54473fdc178c9dc913e
authored: true
---

# update_conjunto

**Módulo:** `api/views/carga_views.py` (líneas 1492-1497)

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
