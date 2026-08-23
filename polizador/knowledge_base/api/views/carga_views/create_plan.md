---
symbol: create_plan
kind: function
module: api/views/carga_views.py
lines: 1566-1567
signature_hash: sha1:88ff7b1e512914f9c868fbc3aa03619605b9b6ee
authored: true
---

# create_plan

**Módulo:** `api/views/carga_views.py` (líneas 1566-1567)

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
