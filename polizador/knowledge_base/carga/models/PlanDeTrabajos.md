---
symbol: PlanDeTrabajos
kind: class
module: carga/models.py
lines: 894-920
signature_hash: sha1:4f05d042b12e792d78cb46c5edd7b1ff8ddd519d
authored: true
---

# PlanDeTrabajos

**Módulo:** `carga/models.py` (líneas 894-920) · hereda de `models.Model`

## Propósito

El plan de trabajos vigente de una Obra: fecha de vigencia, duración en meses
(`trabajos_meses`), y opcionalmente vinculado a un Contrato concreto. Una Obra puede tener
varios `PlanDeTrabajos` a lo largo del tiempo (reprogramaciones) — `vigentes()` es un
`classmethod` que devuelve, para cada Obra, solo el más reciente (mayor `trabajos_fecha`,
`pk` como desempate) vía `Subquery`, y `es_vigente()` lo usa para chequear una instancia
puntual.

## Firma

```python
class PlanDeTrabajos(models.Model):
```

## Uso real

`CrearPlanDeTrabajos` (`carga/views/plandetrabajosviews.py`).

## Ver también

- [Obra](Obra.md)
- [PlanDeTrabajosRubro](PlanDeTrabajosRubro.md)
