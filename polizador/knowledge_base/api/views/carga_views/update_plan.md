---
symbol: update_plan
kind: function
module: api/views/carga_views.py
lines: 1573-1578
signature_hash: sha1:e082caba9e14c1c4c393b7e199f5d4ff55b9d0a9
authored: true
---

# update_plan

**Módulo:** `api/views/carga_views.py` (líneas 1573-1578)

## Propósito

Actualización parcial de un `PlanDeTrabajos` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_plan(request, id: int, payload: PlanDeTrabajosUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`PlanDeTrabajosOut`.

## Ver también

- [PlanDeTrabajos](../../../carga/models/PlanDeTrabajos.md)
