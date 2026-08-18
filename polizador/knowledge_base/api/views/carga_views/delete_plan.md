---
symbol: delete_plan
kind: function
module: api/views/carga_views.py
lines: 1582-1584
signature_hash: sha1:d8c307c2e11dde557d3e36342d0b25c9bdeaef93
authored: true
---

# delete_plan

**Módulo:** `api/views/carga_views.py` (líneas 1582-1584)

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
