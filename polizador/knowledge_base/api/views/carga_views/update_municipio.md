---
symbol: update_municipio
kind: function
module: api/views/carga_views.py
lines: 545-550
signature_hash: sha1:fc0cd53dcd08f3ac374a819b10f5ff1b12303d9b
authored: true
---

# update_municipio

**Módulo:** `api/views/carga_views.py` (líneas 545-550)

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
