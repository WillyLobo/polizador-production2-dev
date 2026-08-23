---
symbol: PlanDeTrabajosEtapaMatriz
kind: class
module: carga/views/plandetrabajosetapaviews.py
lines: 17-114
signature_hash: sha1:c1e6466331488701ed79102ff7ddfed47727e67e
authored: true
---

# PlanDeTrabajosEtapaMatriz

**Módulo:** `carga/views/plandetrabajosetapaviews.py` (líneas 17-114) · hereda de `PermissionRequiredMixin, generic.View`

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

## Firma

```python
class PlanDeTrabajosEtapaMatriz(PermissionRequiredMixin, generic.View):
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
