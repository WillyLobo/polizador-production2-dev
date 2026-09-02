---
symbol: UpdatePlanDeTrabajosRubro
kind: class
module: carga/views/plandetrabajosrubroviews.py
lines: 100-148
signature_hash: sha1:f4985cb54c1c5e449d70749df5039ad20aa85639
authored: true
---

# UpdatePlanDeTrabajosRubro

**Módulo:** `carga/views/plandetrabajosrubroviews.py` (líneas 100-148) · hereda de `LogInvalidFormMixin, PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView`

## Propósito

Edición de un Rubro. `_pedir_foja_numero_inicial()` en edición equivale a "¿se puede seguir editando ese campo?" — solo si el Rubro todavía no tiene ninguna Foja real (no-legacy) cargada, para no romper la numeración ya materializada en la base.

Igual que `CrearPlanDeTrabajosRubro`, `get`/`post` solo fijan `success_url` antes de
delegar en `super()`, así que el registro de `FormValidationError` ante un form inválido
lo dispara solo el hook de `LogInvalidFormMixin`, sin llamada manual.

## Firma

```python
class UpdatePlanDeTrabajosRubro(LogInvalidFormMixin, PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView):
```

## Uso real

`UpdatePlanDeTrabajosRubro` (`carga:update-plandetrabajosrubro`).

## Ver también

- [PlanDeTrabajosRubro](../../models/PlanDeTrabajosRubro.md)
- [CrearPlanDeTrabajosRubro](CrearPlanDeTrabajosRubro.md)
- [FormValidationError](../../../core/models/FormValidationError.md)
