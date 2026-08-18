---
symbol: list_planes
kind: function
module: api/views/carga_views.py
lines: 1551-1555
signature_hash: sha1:b9328d17c5625a816fa5ddf47c0bba823c355801
authored: true
---

# list_planes

**Módulo:** `api/views/carga_views.py` (líneas 1551-1555)

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
