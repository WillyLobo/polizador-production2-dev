---
symbol: PlanDeTrabajosEtapa
kind: class
module: carga/models.py
lines: 1032-1090
signature_hash: sha1:e2a35cec7422d45618a7a37b8fdaa81cf323d0df
authored: true
---
# PlanDeTrabajosEtapa

**Módulo:** `carga/models.py` (líneas 1032-1090) · hereda de `models.Model`

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

## Firma

```python
class PlanDeTrabajosEtapa(models.Model):
```

## Uso real

```python
# carga/views/plandetrabajosetapaviews.py:102 (PlanDeTrabajosEtapaMatriz.post)
etapa = PlanDeTrabajosEtapa.objects.create(etapa_rubro=rubro)
```

## Ver también

- [FojaDeMedicion](FojaDeMedicion.md) — misma estructura, del lado del avance real.
- [add_months](add_months.md)
- [auto_increment_etapa_numero](../signals/auto_increment_etapa_numero.md)
- [PlanDeTrabajosEtapaItem](PlanDeTrabajosEtapaItem.md)