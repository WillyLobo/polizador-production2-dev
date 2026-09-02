---
symbol: list_montos_viaticos
kind: function
module: api/views/secretariador_views.py
lines: 446-450
signature_hash: sha1:78f354c314bd43f242ddaaa51e5ce15ee4e82083
authored: true
---
# list_montos_viaticos

**Módulo:** `api/views/secretariador_views.py` (líneas 446-450)

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