---
symbol: PlanDeTrabajosItem
kind: class
module: carga/models.py
lines: 1261-1295
signature_hash: sha1:eb921c24ab82ece6a149cc24994e1b168079c52e
authored: true
---

# PlanDeTrabajosItem

**Módulo:** `carga/models.py` (líneas 1261-1295) · hereda de `models.Model`

## Propósito

Un item dentro de un Rubro de Plan de Trabajos (ej. "Excavación", "Mampostería"), con su
`planitem_incidencia_pct` (% que representa dentro del rubro). Tiene su propia cadena de
reprogramación paralela a la del Rubro: `item_anterior`/`item_siguiente` (mismo patrón que
`rubro_anterior`/`rubro_siguiente`), recorrida por `item_cadena_ids()`/
`item_cadena_siguiente_ids()`.

Esta cadena a nivel item (no solo a nivel rubro) es la que usa
[recalcular_acumulado_fojas_siguientes](../signals/recalcular_acumulado_fojas_siguientes.md)
para encontrar el `FojaDeMedicionItem` correspondiente en la Foja siguiente — necesita
saber qué item de esa Foja "es el mismo" item, incluso si el Plan se reprogramó y el item
técnicamente es un registro distinto.

## Firma

```python
class PlanDeTrabajosItem(models.Model):
```

## Uso real

`PlanDeTrabajosItemForm` (`carga/forms/plandetrabajositemforms.py`).

## Ver también

- [PlanDeTrabajosRubro](PlanDeTrabajosRubro.md) — mismo patrón de cadena, a nivel rubro.
- [FojaDeMedicionItem](FojaDeMedicionItem.md)
- [recalcular_acumulado_fojas_siguientes](../signals/recalcular_acumulado_fojas_siguientes.md)
