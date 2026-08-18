---
symbol: PlanDeTrabajos
kind: class
module: carga/models.py
lines: 894-920
signature_hash: sha1:4f05d042b12e792d78cb46c5edd7b1ff8ddd519d
authored: false
---

# PlanDeTrabajos

**Módulo:** `carga/models.py` (líneas 894-920)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class PlanDeTrabajos(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:929` — `rubro_plan = models.ForeignKey("PlanDeTrabajos", verbose_name="Plan de Trabajos", on_delete=models.CASCADE, related_name="rubros")`
- `carga/views/ajaxviews.py:56` — `return PlanDeTrabajos.objects.filter(pk=plan_id).first() if plan_id else None`
- `carga/views/obraviews.py:17` — `PlanDeTrabajos,`
- `carga/views/obraviews.py:49` — `queryset=PlanDeTrabajos.objects.prefetch_related(`
- `carga/views/plandetrabajosrubroviews.py:6` — `from carga.models import PlanDeTrabajos, PlanDeTrabajosRubro, ContratoMonto, Certificado`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
