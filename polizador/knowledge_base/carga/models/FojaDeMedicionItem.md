---
symbol: FojaDeMedicionItem
kind: class
module: carga/models.py
lines: 1234-1267
signature_hash: sha1:5f519ce4b22dc3e31567286cd6306bafceb0e16f
authored: false
---

# FojaDeMedicionItem

**Módulo:** `carga/models.py` (líneas 1234-1267)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class FojaDeMedicionItem(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:1202` — `"""Acumulado %% de cada item en la foja anterior (misma lógica que FojaDeMedicionItem.save()).`
- `carga/signals.py:3` — `from .models import FojaDeMedicion, FojaDeMedicionItem, PlanDeTrabajosEtapa, ContratoMonto, ContratoTramoPago`
- `carga/signals.py:41` — `@receiver(post_save, sender=FojaDeMedicionItem)`
- `carga/signals.py:43` — `"""FojaDeMedicionItem.save() calcula fojaitem_pct_acumulado como una copia`
- `carga/signals.py:53` — `item_siguiente = FojaDeMedicionItem.objects.filter(`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
