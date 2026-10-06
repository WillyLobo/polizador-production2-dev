---
symbol: PlanDeTrabajosEtapa
kind: class
module: carga/models.py
lines: 1297-1358
signature_hash: sha1:6dff5567394e98bbb7b8b83a482422c22ea7d06e
authored: true
---
# PlanDeTrabajosEtapa

**Módulo:** `carga/models.py` (líneas 1297-1358) · hereda de `models.Model`

## Propósito

El "gemelo proyectado" de `FojaDeMedicion`: mientras una Foja registra el avance *real*
mes a mes, una Etapa registra el avance *proyectado* — misma estructura de numeración
correlativa por rubro (`etapa_numero`, auto-asignado por
[auto_increment_etapa_numero](../signals/auto_increment_etapa_numero.md)) y misma noción
de "anterior siguiendo la cadena de rubro reprogramado" (`etapa_anterior()`, análogo a
`FojaDeMedicion.foja_anterior()`).

La diferencia real está en `save()`: además de lo que hace la señal de numeración, calcula
`etapa_fecha` a mano — proyecta un mes calendario más que la Etapa anterior
([add_months](add_months.md)), o si es la primera Etapa de la cadena, usa
`etapa_rubro.rubro_plan.trabajos_fecha`. El comentario en el código explica por qué no usa
`self.etapa_anterior()` para esto: esa llamada compararía por `etapa_numero`, que todavía
no está asignado en este punto (la señal `pre_save` corre *dentro* de
`super().save()`, después de este código) — por eso busca "la última etapa de la cadena"
directamente en vez de reusar el método.

Este cálculo de `etapa_fecha` corre sólo si la Etapa llega **sin** fecha. Cuando
`PlanDeTrabajosEtapaMatriz` completa los meses que tienen Foja pero no Etapa en el plan
viejo, crea esas Etapas con `etapa_fecha=foja.foja_periodo`, y `save()` respeta esa fecha
en vez de seguir la cadena.

Ya no existe `anterior_items_map()` en este modelo. El piso que usa la matriz y
`PlanDeTrabajosEtapaItem.save()` en la primera Etapa de un rubro reprogramado es el avance
**real** (`FojaDeMedicion.anterior_items_map()`), no el proyectado del rubro viejo.

## Firma

```python
class PlanDeTrabajosEtapa(models.Model):
```

## Uso real

```python
# carga/views/plandetrabajosetapaviews.py:214 (PlanDeTrabajosEtapaMatriz.post)
etapa = PlanDeTrabajosEtapa.objects.create(etapa_rubro=rubro)
```
Relleno de un mes medido por Foja pero sin Etapa (la fecha viene dada):
```python
# carga/views/plandetrabajosetapaviews.py:210
etapa = PlanDeTrabajosEtapa(etapa_rubro=rubro, etapa_fecha=gap_fojas[col].foja_periodo)
```

## Ver también

- [FojaDeMedicion](FojaDeMedicion.md) — misma estructura, del lado del avance real.
- [add_months](add_months.md)
- [auto_increment_etapa_numero](../signals/auto_increment_etapa_numero.md)
- [PlanDeTrabajosEtapaItem](PlanDeTrabajosEtapaItem.md)