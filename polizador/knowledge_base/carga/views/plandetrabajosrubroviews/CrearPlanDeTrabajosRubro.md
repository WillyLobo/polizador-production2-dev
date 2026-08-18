---
symbol: CrearPlanDeTrabajosRubro
kind: class
module: carga/views/plandetrabajosrubroviews.py
lines: 12-96
signature_hash: sha1:77bc5d7d1fdf7eb6d7b5c9d2ac308b726af8c31a
authored: true
---

# CrearPlanDeTrabajosRubro

**Módulo:** `carga/views/plandetrabajosrubroviews.py` (líneas 12-96) · hereda de `PermissionRequiredMixin, FormsetViewMixin, generic.CreateView`

## Propósito

Alta de un Rubro dentro de un Plan, con su formset inline de Items.
`_pedir_foja_numero_inicial()` decide si mostrar el campo "Número de Foja Inicial": solo
tiene sentido pedirlo cuando este Rubro va a ser necesariamente la raíz de una cadena de
reprogramación (sin `rubro_anterior` posible) *y* la Obra ya tiene Certificados cargados —
en ese caso hace falta indicar desde qué número seguir la numeración de Fojas para no
chocar con historial previo. También acota `rubro_anterior` a Rubros de la misma Obra (en
otro Plan) y `rubro_contratomonto` a los montos del Contrato vinculado al Plan (o de
cualquier Contrato de la Obra si el Plan no tiene uno vinculado).

## Firma

```python
class CrearPlanDeTrabajosRubro(PermissionRequiredMixin, FormsetViewMixin, generic.CreateView):
```

## Uso real

`CrearPlanDeTrabajosRubro` (`carga:crear-plandetrabajosrubro`), enlazada desde la ficha de Plan de Trabajos.

## Ver también

- [PlanDeTrabajosRubro](../../models/PlanDeTrabajosRubro.md)
- [rubroanteriorwidget](../ajaxviews/rubroanteriorwidget.md)
