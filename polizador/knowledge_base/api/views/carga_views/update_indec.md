---
symbol: update_indec
kind: function
module: api/views/carga_views.py
lines: 1809-1814
signature_hash: sha1:dc28149224c490a929f2517eecdacad819d76b2c
authored: true
---

# update_indec

**Módulo:** `api/views/carga_views.py` (líneas 1809-1814)

## Propósito

Actualización parcial de un `INDEC` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_indec(request, id: int, payload: INDECUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`INDECOut`.

## Ver también

- [INDEC](../../../carga/models/INDEC.md)
