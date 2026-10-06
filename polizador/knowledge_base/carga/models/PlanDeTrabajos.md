---
symbol: PlanDeTrabajos
kind: class
module: carga/models.py
lines: 1133-1170
signature_hash: sha1:eb9ea91c9c02ce96f985ea2022eef11a26756fe1
authored: true
---

# PlanDeTrabajos

**Módulo:** `carga/models.py` (líneas 1133-1170) · hereda de `models.Model`

## Propósito

El plan de trabajos vigente de una Obra: fecha de vigencia, duración en meses
(`trabajos_meses`), y opcionalmente vinculado a un Contrato concreto. Una Obra puede tener
varios `PlanDeTrabajos` a lo largo del tiempo (reprogramaciones) — `vigentes()` es un
`classmethod` que devuelve, para cada Obra, solo el más reciente (mayor `trabajos_fecha`,
`pk` como desempate) vía `Subquery`, y `es_vigente()` lo usa para chequear una instancia
puntual.

Dos campos se malinterpretan fácil en una reprogramación:
- `trabajos_meses` es la cantidad de columnas (meses) de la matriz de Etapas proyectadas
  de cada Rubro, **no** la duración total de la obra. Si el Rubro tiene `rubro_anterior`,
  las Etapas nuevas siguen la numeración del rubro viejo. Por eso hay que descontar del
  plazo total las Etapas que ya tenía el plan anterior (no las Fojas medidas, que pueden ser
  más). Los meses medidos por Foja que no tenían Etapa se rellenan solos al abrir la matriz
  y también cuentan dentro de este número.
- `trabajos_fecha_inicio` ("Fecha de Reinicio de Obra") se usa sólo para el reinicio
  después de una reprogramación. El inicio original de la obra es `Obra.obra_fecha_inicio`.

## Firma

```python
class PlanDeTrabajos(models.Model):
```

## Uso real

`CrearPlanDeTrabajos` (`carga/views/plandetrabajosviews.py`).

## Ver también

- [Obra](Obra.md)
- [PlanDeTrabajosRubro](PlanDeTrabajosRubro.md)
