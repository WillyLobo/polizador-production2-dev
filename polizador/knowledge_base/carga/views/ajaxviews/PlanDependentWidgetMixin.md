---
symbol: PlanDependentWidgetMixin
kind: class
module: carga/views/ajaxviews.py
lines: 43-56
signature_hash: sha1:d1f23ffe0dcca8e006bdbaf26d49e2ee2e0a7578
authored: true
---

# PlanDependentWidgetMixin

**Módulo:** `carga/views/ajaxviews.py` (líneas 43-56)

## Propósito

Mixin para widgets usados dentro de `PlanDeTrabajosRubroForm`: acota los resultados AJAX
al Plan de Trabajos elegido en el campo hermano `rubro_plan` del mismo formulario
(`dependent_fields = {"rubro_plan": "rubro_plan_actual"}`, mecanismo de
`django-select2` que reenvía el valor actual de ese campo en cada request AJAX). Por
ejemplo, `contratomontowidget` lo usa para no ofrecer montos de Contratos de *otras* Obras
en el combo de "Monto de Contrato" de un Rubro.

`_plan_actual(dependent_fields)` es el helper compartido que las subclases usan en su
propio `filter_queryset()` para resolver el `PlanDeTrabajos` real a partir del ID
recibido.

## Firma

```python
class PlanDependentWidgetMixin:
```

## Uso real

`class rubroanteriorwidget(PlanDependentWidgetMixin, ...)`, `class contratomontowidget(PlanDependentWidgetMixin, ...)` — ambos en `PlanDeTrabajosRubroForm`.

## Ver también

- [rubroanteriorwidget](rubroanteriorwidget.md)
- [contratomontowidget](contratomontowidget.md)
- [PlanDeTrabajosRubro](../../models/PlanDeTrabajosRubro.md)
