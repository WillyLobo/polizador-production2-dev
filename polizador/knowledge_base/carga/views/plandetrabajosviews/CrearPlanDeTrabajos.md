---
symbol: CrearPlanDeTrabajos
kind: class
module: carga/views/plandetrabajosviews.py
lines: 9-72
signature_hash: sha1:037f46ef5e6f818650154d1215c06ca996ce2ab3
authored: true
---

# CrearPlanDeTrabajos

**Módulo:** `carga/views/plandetrabajosviews.py` (líneas 9-72) · hereda de `PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de un Plan de Trabajos. Soporta clonar un Plan existente vía `?clonar=<id>`: además
de crear el Plan nuevo, `_clonar_desde` copia todos los Rubros e Items del Plan origen,
enlazando cada copia a su original vía `rubro_anterior`/`item_anterior` — es decir, un
"clonar Plan" es en realidad el mecanismo real de **reprogramación** (arranca la cadena
que [PlanDeTrabajosRubro](../../models/PlanDeTrabajosRubro.md) describe), no una copia
independiente.

## Firma

```python
class CrearPlanDeTrabajos(PermissionRequiredMixin, generic.CreateView):
```

## Uso real

```python
# carga/views/plandetrabajosviews.py:58 (_clonar_desde)
rubro_nuevo = PlanDeTrabajosRubro.objects.create(
    rubro_plan=self.object, rubro_nombre=rubro_origen.rubro_nombre, ...,
    rubro_anterior=rubro_origen,
)
```

## Ver también

- [PlanDeTrabajos](../../models/PlanDeTrabajos.md)
- [PlanDeTrabajosRubro](../../models/PlanDeTrabajosRubro.md)
