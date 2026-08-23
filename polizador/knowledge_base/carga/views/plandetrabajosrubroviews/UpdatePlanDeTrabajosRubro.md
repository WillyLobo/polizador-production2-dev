---
symbol: UpdatePlanDeTrabajosRubro
kind: class
module: carga/views/plandetrabajosrubroviews.py
lines: 100-148
signature_hash: sha1:2a425a3aa44bf455c12d2b832b4a1874193fa0a5
authored: true
---

# UpdatePlanDeTrabajosRubro

**Módulo:** `carga/views/plandetrabajosrubroviews.py` (líneas 100-148) · hereda de `PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView`

## Propósito

Edición de un Rubro. `_pedir_foja_numero_inicial()` en edición equivale a "¿se puede seguir editando ese campo?" — solo si el Rubro todavía no tiene ninguna Foja real (no-legacy) cargada, para no romper la numeración ya materializada en la base.

## Firma

```python
class UpdatePlanDeTrabajosRubro(PermissionRequiredMixin, FormsetViewMixin, generic.UpdateView):
```

## Uso real

`UpdatePlanDeTrabajosRubro` (`carga:update-plandetrabajosrubro`).

## Ver también

- [PlanDeTrabajosRubro](../../models/PlanDeTrabajosRubro.md)
- [CrearPlanDeTrabajosRubro](CrearPlanDeTrabajosRubro.md)
