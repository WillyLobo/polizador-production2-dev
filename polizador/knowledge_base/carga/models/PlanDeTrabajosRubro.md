---
symbol: PlanDeTrabajosRubro
kind: class
module: carga/models.py
lines: 922-994
signature_hash: sha1:aa242d5cff239257d7d337c46802c13b0dc627ec
authored: false
---

# PlanDeTrabajosRubro

**Módulo:** `carga/models.py` (líneas 922-994)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class PlanDeTrabajosRubro(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:1003` — `planitem_rubro = models.ForeignKey("PlanDeTrabajosRubro", verbose_name="Rubro de Plan de Trabajos", on_delete=models.CASCADE, related_name="items")`
- `carga/models.py:1042` — `etapa_rubro = models.ForeignKey("PlanDeTrabajosRubro", verbose_name="Rubro de Plan de Trabajos", on_delete=models.CASCADE, related_name="etapas")`
- `carga/models.py:1165` — `foja_rubro = models.ForeignKey("PlanDeTrabajosRubro", verbose_name="Rubro de Plan de Trabajos", on_delete=models.CASCADE, related_name="fojas")`
- `carga/views/ajaxviews.py:120` — `return PlanDeTrabajosRubro.objects.filter(pk=rubro_id).values_list(`
- `carga/views/fojademedicionviews.py:7` — `from carga.models import FojaDeMedicion, PlanDeTrabajosItem, PlanDeTrabajosRubro`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
