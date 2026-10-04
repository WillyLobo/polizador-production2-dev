---
symbol: list_areas
kind: function
module: api/views/carga_views.py
lines: 124-125
signature_hash: sha1:a96697ea41dc83ca4e270d334dc329cfba69ded8
authored: true
---

# list_areas

**Módulo:** `api/views/carga_views.py` (líneas 124-125)

## Propósito

Listado paginado (`PerPagePagination`) de `Area`, gateado por `require_model_perm(Area)` (permiso `view_<modelo>`).

## Firma

```python
def list_areas(request):
```

## Uso real

`GET /v1/api/areas/` — response=`List[AreaOut]`.

## Ver también

- [Area](../../../carga/models/Area.md)
