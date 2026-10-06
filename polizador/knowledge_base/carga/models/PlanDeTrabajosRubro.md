---
symbol: PlanDeTrabajosRubro
kind: class
module: carga/models.py
lines: 1172-1259
signature_hash: sha1:e8424c77a5a0ece89fb98f906de24bf24435984c
authored: true
---

# PlanDeTrabajosRubro

**Módulo:** `carga/models.py` (líneas 1172-1259) · hereda de `models.Model`

## Propósito

Un rubro dentro de un Plan de Trabajos (ej. "Vivienda", "Infraestructura"), con su
presupuesto y, opcionalmente, un `ContratoMonto` vinculado (`monto_base_pesos()`/
`monto_base_uvi()` usan ese monto de contrato si existe, convertido UVI→pesos vía
`Uvi.pesos_equivalentes()`, y si no caen al `rubro_presupuesto` cargado a mano).

Es la pieza que arma la **cadena de reprogramación** que atraviesa buena parte de
`carga`: `rubro_anterior` (FK a sí mismo) enlaza este Rubro con el de un Plan previo del
que es continuación, y `rubro_cadena_ids()`/`rubro_cadena_siguiente_ids()` recorren esa
cadena hacia atrás/adelante respectivamente. Estos dos métodos son la base de la
numeración continua de Fojas/Etapas (`FojaDeMedicion.foja_siguiente()`,
`PlanDeTrabajosEtapa.etapa_anterior()`, las señales
[auto_increment_foja_numero](../signals/auto_increment_foja_numero.md)/
[auto_increment_etapa_numero](../signals/auto_increment_etapa_numero.md)) y del recálculo
en cascada ([recalcular_acumulado_fojas_siguientes](../signals/recalcular_acumulado_fojas_siguientes.md)):
todos ellos filtran por `rubro_id__in=chain_ids` en vez de por un único rubro, para que
una reprogramación no reinicie la numeración ni rompa el recálculo hacia adelante.

`comparacion_etapas_fojas()` pone lado a lado cada Etapa proyectada con la Foja de la misma
posición y calcula el desfasaje (`foja_pct_acumulado() - etapa_pct_proyectado_acumulado()`).
Si se midieron más Fojas que Etapas, las Fojas que sobran se comparan contra la última
Etapa en lugar de quedar sin par. Lo usa `carga/templates/obra/planes-anteriores.html`.

## Firma

```python
class PlanDeTrabajosRubro(models.Model):
```

## Uso real

`PlandeTrabajoForm` (`carga/forms/plandetrabajosforms.py`) para el alta; la reprogramación (asignar `rubro_anterior`) se hace al crear el Rubro del nuevo Plan.

## Ver también

- [PlanDeTrabajosItem](PlanDeTrabajosItem.md) — misma cadena de reprogramación, a nivel de item.
- [FojaDeMedicion](FojaDeMedicion.md)
- [PlanDeTrabajosEtapa](PlanDeTrabajosEtapa.md)
- [ContratoMonto](ContratoMonto.md)
