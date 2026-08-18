---
symbol: PlanDeTrabajosEtapaItem
kind: class
module: carga/models.py
lines: 1116-1153
signature_hash: sha1:91ee171223792a70c27fed056d51df183189ec25
authored: true
---

# PlanDeTrabajosEtapaItem

**Módulo:** `carga/models.py` (líneas 1116-1153) · hereda de `models.Model`

## Propósito

El "gemelo proyectado" de `FojaDeMedicionItem`: mismo patrón de `save()` calculando
`etapaitem_pct_proyectado_acumulado` como copia (anterior + este mes) en vez de un valor
derivado — busca el item correspondiente en la Etapa anterior (`etapa_anterior()`, vía la
cadena de rubro) y le suma su propio `etapaitem_pct_proyectado_mes`.

**Observación real, no documentada en el código:** a diferencia de
`FojaDeMedicionItem`, **no hay ninguna señal que propague el recálculo hacia adelante**
cuando se edita una Etapa anterior — no existe un
`recalcular_acumulado_etapas_siguientes` equivalente a
[recalcular_acumulado_fojas_siguientes](../signals/recalcular_acumulado_fojas_siguientes.md)
en `carga/signals.py`. En la práctica esto probablemente no genera inconsistencias porque
`PlanDeTrabajosEtapaMatriz` (la única vista que las crea/edita) siempre reguarda *todas*
las Etapas del rubro de una sola vez en la grilla — pero si alguna vez se edita una sola
Etapa vieja por fuera de esa vista, las posteriores quedarían con el acumulado
desactualizado, igual que le pasaba a `FojaDeMedicionItem` antes de esa señal.

## Firma

```python
class PlanDeTrabajosEtapaItem(models.Model):
```

## Uso real

```python
# carga/views/plandetrabajosetapaviews.py:111 (PlanDeTrabajosEtapaMatriz.post)
etapaitem.save()  # recalcula etapaitem_pct_proyectado_acumulado, sin disparar cascada hacia adelante
```

## Ver también

- [FojaDeMedicionItem](FojaDeMedicionItem.md) — mismo patrón de `save()`, pero con cascada vía señal.
- [recalcular_acumulado_fojas_siguientes](../signals/recalcular_acumulado_fojas_siguientes.md) — la señal que este modelo NO tiene un equivalente.
- [PlanDeTrabajosEtapa](PlanDeTrabajosEtapa.md)
