---
symbol: create_plan
kind: function
module: api/views/carga_views.py
lines: 1567-1568
signature_hash: sha1:608e5805684bba40385d3df3236d329dba3123ec
authored: true
---

# create_plan

**Módulo:** `api/views/carga_views.py` (líneas 1567-1568)

## Propósito

Alta de `PlanDeTrabajos` desde `PlanDeTrabajosCreate` (`payload.model_dump()` directo a `PlanDeTrabajos.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_plan(request, payload: PlanDeTrabajosCreate):
```

## Uso real

`POST /v1/api/planes/` — response=`PlanDeTrabajosOut`.

## Ver también

- [PlanDeTrabajos](../../../carga/models/PlanDeTrabajos.md)
