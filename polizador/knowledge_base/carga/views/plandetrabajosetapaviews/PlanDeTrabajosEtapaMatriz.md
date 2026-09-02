---
symbol: PlanDeTrabajosEtapaMatriz
kind: class
module: carga/views/plandetrabajosetapaviews.py
lines: 18-116
signature_hash: sha1:4304f710cd31f5ea83130f8944ea802e8a26c42b
authored: true
---

# PlanDeTrabajosEtapaMatriz

**Módulo:** `carga/views/plandetrabajosetapaviews.py` (líneas 18-116) · hereda de `LogInvalidFormMixin, PermissionRequiredMixin, generic.View`

## Propósito

Carga/edita de una sola vez **todas** las Etapas Proyectadas de un Rubro, con una grilla
fila=item / columna=etapa(mes) — la reproducción digital de la planilla de origen en
papel. `_get_anterior_map` tiene una advertencia propia en su docstring: como la matriz
edita de una sola vez las etapas existentes *y* las nuevas, el acumulado anterior tiene
que excluir la etapa existente más reciente (si no, se contaría dos veces: una vía
`anterior_map`, otra como columna de la matriz).

El `post` es la única vista de `carga` que crea/actualiza `PlanDeTrabajosEtapa` y
`PlanDeTrabajosEtapaItem` en bloque dentro de una `transaction.atomic()`: por cada
columna sin Etapa existente, crea una (disparando
[auto_increment_etapa_numero](../../signals/auto_increment_etapa_numero.md)), y para cada
celda hace `get_or_create` + `save()` explícito del `PlanDeTrabajosEtapaItem` — ver la
nota sobre la ausencia de cascada hacia adelante en esa página del modelo.

Al ser `generic.View` puro (no `FormView`/`FormsetViewMixin`), tampoco pasa por el hook
automático de `LogInvalidFormMixin`; el `post()` invoca `self._log_form_debug(form)` a
mano cuando `build_matriz_form` no valida.

## Firma

```python
class PlanDeTrabajosEtapaMatriz(LogInvalidFormMixin, PermissionRequiredMixin, generic.View):
```

## Uso real

```python
# carga/views/plandetrabajosetapaviews.py:102
etapa = PlanDeTrabajosEtapa.objects.create(etapa_rubro=rubro)
...
etapaitem.save()
```

## Ver también

- [PlanDeTrabajosEtapa](../../models/PlanDeTrabajosEtapa.md)
- [PlanDeTrabajosEtapaItem](../../models/PlanDeTrabajosEtapaItem.md)
- [auto_increment_etapa_numero](../../signals/auto_increment_etapa_numero.md)
- [FormValidationError](../../../core/models/FormValidationError.md)
