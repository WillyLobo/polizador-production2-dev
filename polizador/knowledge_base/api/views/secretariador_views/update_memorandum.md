---
symbol: update_memorandum
kind: function
module: api/views/secretariador_views.py
lines: 77-82
signature_hash: sha1:e83f421734cd42353dae68e1c472e556b976a370
authored: true
---

# update_memorandum

**Módulo:** `api/views/secretariador_views.py` (líneas 77-82)

## Propósito

Actualización parcial de un `InstrumentosLegalesMemorandum` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_memorandum(request, id: int, payload: MemorandumUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`InstrumentosLegalesMemorandumOut`.

## Ver también

- [InstrumentosLegalesMemorandum](../../../secretariador/models/InstrumentosLegalesMemorandum.md)
