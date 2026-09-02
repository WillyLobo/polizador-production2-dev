---
symbol: CrearPlanDeTrabajos
kind: class
module: carga/views/plandetrabajosviews.py
lines: 10-73
signature_hash: sha1:7d0bd12200e192f9e97ef91cb757f7041426e9ee
authored: true
---

# CrearPlanDeTrabajos

**Módulo:** `carga/views/plandetrabajosviews.py` (líneas 10-73) · hereda de `LogInvalidFormMixin, PermissionRequiredMixin, generic.CreateView`

## Propósito

Alta de un Plan de Trabajos. Soporta clonar un Plan existente vía `?clonar=<id>`: además
de crear el Plan nuevo, `_clonar_desde` copia todos los Rubros e Items del Plan origen,
enlazando cada copia a su original vía `rubro_anterior`/`item_anterior` — es decir, un
"clonar Plan" es en realidad el mecanismo real de **reprogramación** (arranca la cadena
que [PlanDeTrabajosRubro](../../models/PlanDeTrabajosRubro.md) describe), no una copia
independiente.

Es un `CreateView` estándar (sin `post()` propio), así que el `form_invalid()`
automático de `LogInvalidFormMixin` alcanza para loguear un form inválido — no necesita
invocar `_log_form_debug` a mano.

## Firma

```python
class CrearPlanDeTrabajos(LogInvalidFormMixin, PermissionRequiredMixin, generic.CreateView):
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
- [FormValidationError](../../../core/models/FormValidationError.md)
