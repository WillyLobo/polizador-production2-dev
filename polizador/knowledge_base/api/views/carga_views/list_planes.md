---
symbol: list_planes
kind: function
module: api/views/carga_views.py
lines: 1552-1556
signature_hash: sha1:331e4ab1d28e16bec321825a77228aa9f6bf7f0e
authored: true
---

# list_planes

**Módulo:** `api/views/carga_views.py` (líneas 1552-1556)

## Propósito

Listado paginado (`PerPagePagination`) de `PlanDeTrabajos`, gateado por `require_model_perm(PlanDeTrabajos)` (permiso `view_<modelo>`). Con `?obra=` para acotar a una Obra.

## Firma

```python
def list_planes(request, obra: str=''):
```

## Uso real

`GET /v1/api/planes/` — response=`List[PlanDeTrabajosOut]`.

## Ver también

- [PlanDeTrabajos](../../../carga/models/PlanDeTrabajos.md)
