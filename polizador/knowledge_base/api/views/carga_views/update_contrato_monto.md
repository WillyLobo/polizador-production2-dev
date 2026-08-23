---
symbol: update_contrato_monto
kind: function
module: api/views/carga_views.py
lines: 1646-1651
signature_hash: sha1:fff987b1a8d0f2f6b2ce5cd67b16bcc684bd3acd
authored: true
---

# update_contrato_monto

**Módulo:** `api/views/carga_views.py` (líneas 1646-1651)

## Propósito

Actualización parcial de un `ContratoMonto` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_contrato_monto(request, id: int, payload: ContratoMontoUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`ContratoMontoOut`.

## Ver también

- [ContratoMonto](../../../carga/models/ContratoMonto.md)
