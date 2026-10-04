---
symbol: update_contrato_digital
kind: function
module: api/views/carga_views.py
lines: 1729-1734
signature_hash: sha1:1904f16b4319390dcbaa8223262fb751211a52a8
authored: true
---

# update_contrato_digital

**Módulo:** `api/views/carga_views.py` (líneas 1729-1734)

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
