---
symbol: PlanDeTrabajosRubro
kind: class
module: carga/models.py
lines: 922-994
signature_hash: sha1:aa242d5cff239257d7d337c46802c13b0dc627ec
authored: true
---

# PlanDeTrabajosRubro

**Módulo:** `carga/models.py` (líneas 922-994) · hereda de `models.Model`

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
