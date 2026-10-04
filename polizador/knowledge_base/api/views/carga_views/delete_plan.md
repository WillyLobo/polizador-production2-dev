---
symbol: delete_plan
kind: function
module: api/views/carga_views.py
lines: 1583-1585
signature_hash: sha1:21c746c2132bb6fa5edf24a619b03de3c719860a
authored: true
---

# delete_plan

**Módulo:** `api/views/carga_views.py` (líneas 1583-1585)

## Propósito

Borrado físico (no soft-delete) de un `PlanDeTrabajos` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_plan(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [PlanDeTrabajos](../../../carga/models/PlanDeTrabajos.md)
