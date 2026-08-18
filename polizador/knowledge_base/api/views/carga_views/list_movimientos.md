---
symbol: list_movimientos
kind: function
module: api/views/carga_views.py
lines: 1912-1915
signature_hash: sha1:198557abeaaba821b09d27f0ae179450f2f05c09
authored: true
---

# list_movimientos

**Módulo:** `api/views/carga_views.py` (líneas 1912-1915)

## Propósito

Listado paginado (`PerPagePagination`) de `Poliza_Movimiento`, gateado por `require_model_perm(Poliza_Movimiento)` (permiso `view_<modelo>`).

## Firma

```python
def list_movimientos(request):
```

## Uso real

`GET /v1/api/movimientos/` — response=`List[Poliza_MovimientoOut]`.

## Ver también

- [Poliza_Movimiento](../../../carga/models/Poliza_Movimiento.md)
- [Poliza](../../../carga/models/Poliza.md)
