---
symbol: CrearPlanDeTrabajosRubro
kind: class
module: carga/views/plandetrabajosrubroviews.py
lines: 12-96
signature_hash: sha1:47b23a4569eeaacce3af7d8c4aeb8527af23263b
authored: true
---

# CrearPlanDeTrabajosRubro

**Módulo:** `carga/views/plandetrabajosrubroviews.py` (líneas 12-96) · hereda de `LogInvalidFormMixin, PermissionRequiredMixin, FormsetViewMixin, generic.CreateView`

## Propósito

Alta de un Rubro dentro de un Plan, con su formset inline de Items.
`_pedir_foja_numero_inicial()` decide si mostrar el campo "Número de Foja Inicial": solo
tiene sentido pedirlo cuando este Rubro va a ser necesariamente la raíz de una cadena de
reprogramación (sin `rubro_anterior` posible) *y* la Obra ya tiene Certificados cargados —
en ese caso hace falta indicar desde qué número seguir la numeración de Fojas para no
chocar con historial previo. También acota `rubro_anterior` a Rubros de la misma Obra (en
otro Plan) y `rubro_contratomonto` a los montos del Contrato vinculado al Plan (o de
cualquier Contrato de la Obra si el Plan no tiene uno vinculado).

A diferencia de `CrearFojaDeMedicion`, su `get`/`post` propios solo fijan `success_url`
antes de delegar en `super()` (`FormsetViewMixin`), así que el hook automático de
`LogInvalidFormMixin.form_invalid()` sí se dispara solo — no hace falta (ni hay) una
llamada manual a `_log_form_debug`.

## Firma

```python
class CrearPlanDeTrabajosRubro(LogInvalidFormMixin, PermissionRequiredMixin, FormsetViewMixin, generic.CreateView):
```

## Uso real

`CrearPlanDeTrabajosRubro` (`carga:crear-plandetrabajosrubro`), enlazada desde la ficha de Plan de Trabajos.

## Ver también

- [PlanDeTrabajosRubro](../../models/PlanDeTrabajosRubro.md)
- [rubroanteriorwidget](../ajaxviews/rubroanteriorwidget.md)
- [FormValidationError](../../../core/models/FormValidationError.md)
