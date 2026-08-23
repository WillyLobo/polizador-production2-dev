---
symbol: update_municipio
kind: function
module: api/views/carga_views.py
lines: 544-549
signature_hash: sha1:36789697a632647109187a209ce2d87d1e74a34e
authored: true
---

# update_municipio

**Módulo:** `api/views/carga_views.py` (líneas 544-549)

## Propósito

Actualización parcial de un `Municipio` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_municipio(request, id: int, payload: MunicipioUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`MunicipioOut`.

## Ver también

- [Municipio](../../../carga/models/Municipio.md)
