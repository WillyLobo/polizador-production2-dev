---
symbol: list_areas
kind: function
module: api/views/carga_views.py
lines: 123-124
signature_hash: sha1:11847fa3662146dcafc1b765c6aed06d772225dd
authored: true
---

# list_areas

**Módulo:** `api/views/carga_views.py` (líneas 123-124)

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
