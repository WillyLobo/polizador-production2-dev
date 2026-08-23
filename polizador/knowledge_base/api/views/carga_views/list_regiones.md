---
symbol: list_regiones
kind: function
module: api/views/carga_views.py
lines: 402-403
signature_hash: sha1:b32f8f66ac4ef20f3d7c984e77c907b23c9a6490
authored: true
---

# list_regiones

**Módulo:** `api/views/carga_views.py` (líneas 402-403)

## Propósito

Listado paginado (`PerPagePagination`) de `Region`, gateado por `require_model_perm(Region)` (permiso `view_<modelo>`).

## Firma

```python
def list_regiones(request):
```

## Uso real

`GET /v1/api/regiones/` — response=`List[RegionOut]`.

## Ver también

- [Region](../../../carga/models/Region.md)
