---
symbol: retrieve_plan
kind: function
module: api/views/carga_views.py
lines: 1561-1562
signature_hash: sha1:43afa26669bd68c85e7deeeb47be907c8bcc6ac9
authored: true
---

# retrieve_plan

**Módulo:** `api/views/carga_views.py` (líneas 1561-1562)

## Propósito

Devuelve un `PlanDeTrabajos` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_plan(request, id: int):
```

## Uso real

`GET /v1/api/plane/{{id}}/` — response=`PlanDeTrabajosOut`.

## Ver también

- [PlanDeTrabajos](../../../carga/models/PlanDeTrabajos.md)
