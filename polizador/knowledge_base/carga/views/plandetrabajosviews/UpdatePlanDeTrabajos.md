---
symbol: UpdatePlanDeTrabajos
kind: class
module: carga/views/plandetrabajosviews.py
lines: 76-86
signature_hash: sha1:31c052bd61571c4fc285ff1dced4adc07982ab4c
authored: true
---

# UpdatePlanDeTrabajos

**Módulo:** `carga/views/plandetrabajosviews.py` (líneas 76-86) · hereda de `LogInvalidFormMixin, PermissionRequiredMixin, generic.UpdateView`

## Propósito

Edición de Plan de Trabajos; acota el combo de `trabajos_contrato` a los Contratos de la misma Obra.

`UpdateView` estándar sin `post()` propio: el `form_invalid()` automático de
`LogInvalidFormMixin` se encarga de loguear un form inválido.

## Firma

```python
class UpdatePlanDeTrabajos(LogInvalidFormMixin, PermissionRequiredMixin, generic.UpdateView):
```

## Uso real

`UpdatePlanDeTrabajos` (`carga:update-plandetrabajos`).

## Ver también

- [PlanDeTrabajos](../../models/PlanDeTrabajos.md)
- [FormValidationError](../../../core/models/FormValidationError.md)
