---
symbol: PlanDeTrabajosEtapa
kind: class
module: carga/models.py
lines: 1032-1114
signature_hash: sha1:e4ebd80e77dc4460ba8cf926ab3d9be9c5580aa8
authored: false
---

# PlanDeTrabajosEtapa

**Módulo:** `carga/models.py` (líneas 1032-1114)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class PlanDeTrabajosEtapa(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:1124` — `etapaitem_etapa = models.ForeignKey("PlanDeTrabajosEtapa", verbose_name="Etapa Proyectada", on_delete=models.CASCADE, related_name="items")`
- `carga/signals.py:3` — `from .models import FojaDeMedicion, FojaDeMedicionItem, PlanDeTrabajosEtapa, ContratoMonto, ContratoTramoPago`
- `carga/signals.py:29` — `@receiver(pre_save, sender=PlanDeTrabajosEtapa)`
- `carga/signals.py:34` — `last_etapa = PlanDeTrabajosEtapa.objects.filter(`
- `carga/views/certificadoviews.py:23` — `from carga.models import Certificado, CertificadoFinanciamiento, ContratoMonto, FojaDeMedicion, PlanDeTrabajosEtapa, Uvi`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
