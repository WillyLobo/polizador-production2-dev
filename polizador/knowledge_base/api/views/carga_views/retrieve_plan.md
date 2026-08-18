---
symbol: retrieve_plan
kind: function
module: api/views/carga_views.py
lines: 1560-1561
signature_hash: sha1:8e85ff0428126f0751fd24d2860fe7046fb87719
authored: true
---

# retrieve_plan

**Módulo:** `api/views/carga_views.py` (líneas 1560-1561)

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
