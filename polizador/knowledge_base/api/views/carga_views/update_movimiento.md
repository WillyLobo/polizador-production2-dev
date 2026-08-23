---
symbol: update_movimiento
kind: function
module: api/views/carga_views.py
lines: 1932-1937
signature_hash: sha1:dcef7d75fba467eefa9e861938ceb90f61998826
authored: true
---

# update_movimiento

**Módulo:** `api/views/carga_views.py` (líneas 1932-1937)

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
