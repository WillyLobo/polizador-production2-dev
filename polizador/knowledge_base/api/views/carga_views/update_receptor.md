---
symbol: update_receptor
kind: function
module: api/views/carga_views.py
lines: 105-110
signature_hash: sha1:d57de34065c0592126ec6829cbf95d7891ce838d
authored: true
---

# update_receptor

**Módulo:** `api/views/carga_views.py` (líneas 105-110)

## Propósito

Actualización parcial de un `Receptor` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_receptor(request, id: int, payload: ReceptorUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`ReceptorOut`.

## Ver también

- [Receptor](../../../carga/models/Receptor.md)
