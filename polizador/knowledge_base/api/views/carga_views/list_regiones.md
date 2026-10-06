---
symbol: list_regiones
kind: function
module: api/views/carga_views.py
lines: 403-404
signature_hash: sha1:23ba4a4b455e3ddb0866dcabe17c201bb98cb216
authored: true
---

# list_regiones

**Módulo:** `api/views/carga_views.py` (líneas 403-404)

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
