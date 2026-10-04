---
symbol: PlanDeTrabajosEtapaMatriz
kind: class
module: carga/views/plandetrabajosetapaviews.py
lines: 18-240
signature_hash: sha1:b822d68e36653111d6e8b782f8d630684908578c
authored: true
---

# PlanDeTrabajosEtapaMatriz

**Módulo:** `carga/views/plandetrabajosetapaviews.py` (líneas 18-240) · hereda de `LogInvalidFormMixin, PermissionRequiredMixin, generic.View`

## Propósito

Carga/edita de una sola vez **todas** las Etapas Proyectadas de un Rubro, con una grilla
fila=item / columna=etapa(mes) — la reproducción digital de la planilla de origen en
papel.

**Solo lectura si el plan no es el vigente.** `_es_readonly()` (=`not
rubro_plan.es_vigente()`) deshabilita todos los inputs en el `GET` y hace que el `post`
devuelva `403`. Para seguir cargando avance en una obra reprogramada se crea un plan nuevo,
no se reabre el viejo.

**Rubros reprogramados: historial y relleno del "hueco".** Si el Rubro tiene
`rubro_anterior`, `_get_historial_y_gap()` toma las Fojas de toda la cadena predecesora y
las separa:
- *historial*: las primeras N Fojas, una por cada Etapa que llegó a tener el plan viejo.
  Se muestran como columnas de solo lectura con el `%` real del mes.
- *gap*: las Fojas medidas **después** de que el plan viejo dejó de proyectar (hay más
  Fojas que Etapas). Se ofrecen como primeras columnas de la grilla, precargadas con el
  avance real y bloqueadas. Al guardar, se crea una Etapa por cada una con
  `etapa_fecha=foja.foja_periodo`, y su `etapaitem_pct_proyectado_acumulado` se corrige
  con un `update()` al acumulado real de esa Foja. El fallback de
  `PlanDeTrabajosEtapaItem.save()` lo calcularía contra la última Foja de toda la cadena.

El hueco **no** se rellena si ya se emitió algún Certificado por Foja en la cadena
predecesora (`_certificados_ya_emitidos()`). `ley27397.resolver_tasas_periodo` recalcula el
reparto FIFO desde la primera Foja en cada llamada, y completar meses después de haber
certificado podría resolver distinto hacia adelante. En ese caso esas Fojas pasan al
historial y el template muestra un aviso (`gap_bloqueado_por_certificados`).

`_get_anterior_map` es el piso de cada item y se basa en el avance **real** (Fojas), no en
lo proyectado por el rubro anterior (que siempre llega al 100% de la incidencia). Si hay
historial, el piso se corta en la última Foja de historial y no en la última de toda la
cadena: los meses posteriores ya son columnas de la grilla, y contarlos también en el piso
duplicaría el acumulado. `total_columns` es el máximo entre `trabajos_meses`, las etapas
existentes y las columnas de hueco.

El `post` es la única vista de `carga` que crea/actualiza `PlanDeTrabajosEtapa` y
`PlanDeTrabajosEtapaItem` en bloque dentro de una `transaction.atomic()`: por cada
columna sin Etapa existente, crea una (disparando
[auto_increment_etapa_numero](../../signals/auto_increment_etapa_numero.md)), y para cada
celda hace `get_or_create` + `save()` explícito del `PlanDeTrabajosEtapaItem` — ver la
nota sobre la ausencia de cascada hacia adelante en esa página del modelo. Al terminar
redirige a la ficha de la Obra.

Al ser `generic.View` puro (no `FormView`/`FormsetViewMixin`), tampoco pasa por el hook
automático de `LogInvalidFormMixin`; el `post()` invoca `self._log_form_debug(form)` a
mano cuando `build_matriz_form` no valida. Pasa `historial_object=rubro_plan` para que la
barra lateral de historial muestre la historia del Plan.

## Firma

```python
class PlanDeTrabajosEtapaMatriz(LogInvalidFormMixin, PermissionRequiredMixin, generic.View):
```

## Uso real

```python
# carga/views/plandetrabajosetapaviews.py:207-214 (post, dentro de transaction.atomic())
if col < len(etapas):
    etapa = etapas[col]
elif col < len(gap_fojas):
    etapa = PlanDeTrabajosEtapa(etapa_rubro=rubro, etapa_fecha=gap_fojas[col].foja_periodo)
    etapa.save()
else:
    etapa = PlanDeTrabajosEtapa.objects.create(etapa_rubro=rubro)
...
etapaitem.save()
```

## Ver también

- [PlanDeTrabajosEtapa](../../models/PlanDeTrabajosEtapa.md)
- [PlanDeTrabajosEtapaItem](../../models/PlanDeTrabajosEtapaItem.md)
- [auto_increment_etapa_numero](../../signals/auto_increment_etapa_numero.md)
- [FormValidationError](../../../core/models/FormValidationError.md)

- [PlanDeTrabajos](../../models/PlanDeTrabajos.md) — `es_vigente()` y `trabajos_meses`.
- [FojaDeMedicion](../../models/FojaDeMedicion.md)
