---
symbol: create_movimiento
kind: function
module: api/views/carga_views.py
lines: 1947-1948
signature_hash: sha1:1053ed3a50f9e054d0d0ff2396bba144d23ce86f
authored: true
---

# create_movimiento

**Módulo:** `api/views/carga_views.py` (líneas 1947-1948)

## Propósito

Alta de `Poliza_Movimiento` desde `Poliza_MovimientoCreate` (`payload.model_dump()` directo a `Poliza_Movimiento.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_movimiento(request, payload: PolizaMovimientoCreate):
```

## Uso real

`POST /v1/api/movimientos/` — response=`Poliza_MovimientoOut`.

## Ver también

- [Poliza_Movimiento](../../../carga/models/Poliza_Movimiento.md)
- [Poliza](../../../carga/models/Poliza.md)
