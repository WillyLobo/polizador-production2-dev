---
symbol: create_movimiento
kind: function
module: api/views/carga_views.py
lines: 1926-1927
signature_hash: sha1:5d746dd1ef1dd044e10f8085bd6cf18b416f8634
authored: true
---

# create_movimiento

**Módulo:** `api/views/carga_views.py` (líneas 1926-1927)

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
