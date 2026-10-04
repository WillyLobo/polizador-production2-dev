---
symbol: add_months
kind: function
module: carga/models.py
lines: 22-28
signature_hash: sha1:3a7c86a2c7222f1841dc6f95c391e55debac01e6
authored: true
---

# add_months

**Módulo:** `carga/models.py` (líneas 22-28)

## Propósito

Suma `n` meses a una fecha, ajustando el día si el mes destino tiene menos días (ej. 31
de enero + 1 mes → 28/29 de febrero, no un "3 de marzo" corrido por desborde). Es la única
función de este módulo que no es un modelo ni un `upload_to`: existe porque
`PlanDeTrabajosEtapa.save()` necesita proyectar la fecha de cada Etapa mensual a partir de
la fecha de la Etapa anterior, y `timedelta(days=30)` no sirve para "un mes calendario".

## Firma

```python
def add_months(fecha, n):
```

## Uso real

```python
# carga/models.py:1087 (PlanDeTrabajosEtapa.save())
self.etapa_fecha = add_months(anterior.etapa_fecha, 1) if anterior else self.etapa_rubro.rubro_plan.trabajos_fecha
```

## Ver también

- [PlanDeTrabajosEtapa](PlanDeTrabajosEtapa.md) — única llamadora.
