---
symbol: update_uvi
kind: function
module: api/views/carga_views.py
lines: 1748-1753
signature_hash: sha1:fd389321e95e88843d3365e10932d61d6c6acbf2
authored: true
---

# update_uvi

**Módulo:** `api/views/carga_views.py` (líneas 1748-1753)

## Propósito

Actualización parcial de un `Uvi` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_uvi(request, id: int, payload: UviUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`UviOut`.

## Ver también

- [Uvi](../../../carga/models/Uvi.md)
