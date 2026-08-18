---
symbol: update_contrato_digital
kind: function
module: api/views/carga_views.py
lines: 1708-1713
signature_hash: sha1:9e0df0fec0dd9b883545150ae8de0635d5fafc1e
authored: true
---

# update_contrato_digital

**Módulo:** `api/views/carga_views.py` (líneas 1708-1713)

## Propósito

Actualización parcial de un `ContratosDigitales` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_contrato_digital(request, id: int, payload: ContratosDigitalesUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`ContratosDigitalesOut`.

## Ver también

- [ContratosDigitales](../../../carga/models/ContratosDigitales.md)
