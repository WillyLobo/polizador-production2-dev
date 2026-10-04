---
symbol: retrieve_movimiento
kind: function
module: api/views/carga_views.py
lines: 1941-1942
signature_hash: sha1:7016b735d7cf0d8117f1116ece83680c90115ae2
authored: true
---

# retrieve_movimiento

**Módulo:** `api/views/carga_views.py` (líneas 1941-1942)

## Propósito

Devuelve un `Poliza_Movimiento` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_movimiento(request, id: int):
```

## Uso real

`GET /v1/api/movimiento/{{id}}/` — response=`Poliza_MovimientoOut`.

## Ver también

- [Poliza_Movimiento](../../../carga/models/Poliza_Movimiento.md)
- [Poliza](../../../carga/models/Poliza.md)
