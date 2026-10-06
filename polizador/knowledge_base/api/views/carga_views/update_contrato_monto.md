---
symbol: update_contrato_monto
kind: function
module: api/views/carga_views.py
lines: 1667-1672
signature_hash: sha1:87191919e02057c46e26c53e6d11bd364a268906
authored: true
---

# update_contrato_monto

**Módulo:** `api/views/carga_views.py` (líneas 1667-1672)

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
