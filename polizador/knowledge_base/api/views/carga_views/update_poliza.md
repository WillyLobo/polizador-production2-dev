---
symbol: update_poliza
kind: function
module: api/views/carga_views.py
lines: 1851-1856
signature_hash: sha1:79ce2301c755384d47b2352bb4486521fbee3c68
authored: true
---

# update_poliza

**Módulo:** `api/views/carga_views.py` (líneas 1851-1856)

## Propósito

Actualización parcial de un `Poliza` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_poliza(request, id: int, payload: PolizaUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`PolizaOut`.

## Ver también

- [Poliza](../../../carga/models/Poliza.md)
