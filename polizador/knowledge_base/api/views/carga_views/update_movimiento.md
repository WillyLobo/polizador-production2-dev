---
symbol: update_movimiento
kind: function
module: api/views/carga_views.py
lines: 1953-1958
signature_hash: sha1:dde614b54dc259b046dfe4bed987e14b049f9046
authored: true
---

# update_movimiento

**Módulo:** `api/views/carga_views.py` (líneas 1953-1958)

## Propósito

Actualización parcial de un `Poliza_Movimiento` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_movimiento(request, id: int, payload: PolizaMovimientoUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`Poliza_MovimientoOut`.

## Ver también

- [Poliza_Movimiento](../../../carga/models/Poliza_Movimiento.md)
- [Poliza](../../../carga/models/Poliza.md)
