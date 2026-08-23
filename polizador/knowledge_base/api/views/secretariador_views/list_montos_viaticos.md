---
symbol: list_montos_viaticos
kind: function
module: api/views/secretariador_views.py
lines: 439-443
signature_hash: sha1:e969cb9ebab254498f97af0ae6c3eb70300c61dc
authored: true
---

# list_montos_viaticos

**Módulo:** `api/views/secretariador_views.py` (líneas 439-443)

## Propósito

Listado paginado (`PerPagePagination`) de `MontoViaticoDiario`, gateado por `require_model_perm(MontoViaticoDiario)` (permiso `view_<modelo>`). Con `?decreto=` para acotar a un Decreto. Sin `retrieve`/`update`.

## Firma

```python
def list_montos_viaticos(request, decreto: str=''):
```

## Uso real

`GET /v1/api/montos-viaticos/` — response=`List[MontoViaticoDiarioOut]`.

## Ver también

- [MontoViaticoDiario](../../../secretariador/models/MontoViaticoDiario.md)
