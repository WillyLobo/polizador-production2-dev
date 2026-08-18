---
symbol: list_provincias
kind: function
module: api/views/carga_views.py
lines: 365-366
signature_hash: sha1:b455263d11f25eb6c5ad45ff88a9135d2f062bc3
authored: true
---

# list_provincias

**Módulo:** `api/views/carga_views.py` (líneas 365-366)

## Propósito

Listado paginado (`PerPagePagination`) de `Provincia`, gateado por `require_model_perm(Provincia)` (permiso `view_<modelo>`).

## Firma

```python
def list_provincias(request):
```

## Uso real

`GET /v1/api/provincias/` — response=`List[ProvinciaOut]`.

## Ver también

- [Provincia](../../../carga/models/Provincia.md)
