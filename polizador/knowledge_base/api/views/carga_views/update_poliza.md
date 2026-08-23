---
symbol: update_poliza
kind: function
module: api/views/carga_views.py
lines: 1830-1835
signature_hash: sha1:4b19310064b7ec4b3f4955cf3ec67ea9c80eee43
authored: true
---

# update_poliza

**Módulo:** `api/views/carga_views.py` (líneas 1830-1835)

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
