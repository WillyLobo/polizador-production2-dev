---
symbol: update_plan
kind: function
module: api/views/carga_views.py
lines: 1572-1577
signature_hash: sha1:4eeff28133552142742e40813cb57a62abc7d3ff
authored: true
---

# update_plan

**Módulo:** `api/views/carga_views.py` (líneas 1572-1577)

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
