---
symbol: UpdatePlanDeTrabajos
kind: class
module: carga/views/plandetrabajosviews.py
lines: 75-85
signature_hash: sha1:fb43b56d34825cb5858d8aa2463ba6de4cdc1ee8
authored: true
---

# UpdatePlanDeTrabajos

**Módulo:** `carga/views/plandetrabajosviews.py` (líneas 75-85) · hereda de `PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de Plan de Trabajos; acota el combo de `trabajos_contrato` a los Contratos de la misma Obra.

## Firma

```python
class UpdatePlanDeTrabajos(PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdatePlanDeTrabajos` (`carga:update-plandetrabajos`).

## Ver también

- [PlanDeTrabajos](../../models/PlanDeTrabajos.md)
