---
symbol: PlanDeTrabajosItem
kind: class
module: carga/models.py
lines: 996-1030
signature_hash: sha1:bbc55790ecc79dda524420ce9f1942cfd5e5be92
authored: false
---

# PlanDeTrabajosItem

**Módulo:** `carga/models.py` (líneas 996-1030)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class PlanDeTrabajosItem(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:1067` — `items = PlanDeTrabajosItem.objects.filter(planitem_rubro=rubro)`
- `carga/models.py:1125` — `etapaitem_planitem = models.ForeignKey("PlanDeTrabajosItem", verbose_name="Item del Plan", on_delete=models.CASCADE)`
- `carga/models.py:1217` — `items = PlanDeTrabajosItem.objects.filter(planitem_rubro=rubro)`
- `carga/models.py:1243` — `fojaitem_planitem = models.ForeignKey("PlanDeTrabajosItem", verbose_name="Item del Plan", on_delete=models.CASCADE)`
- `carga/views/fojademedicionviews.py:7` — `from carga.models import FojaDeMedicion, PlanDeTrabajosItem, PlanDeTrabajosRubro`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
