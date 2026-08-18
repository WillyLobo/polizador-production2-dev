---
symbol: FojaDeMedicion
kind: class
module: carga/models.py
lines: 1155-1232
signature_hash: sha1:5ddfe3e2ae7c898fb17e02b7a9997879e87db835
authored: false
---

# FojaDeMedicion

**Módulo:** `carga/models.py` (líneas 1155-1232)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class FojaDeMedicion(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:787` — `certificado_foja = models.ForeignKey("FojaDeMedicion", verbose_name="Foja de Medición de Origen", on_delete=models.SET_NULL, null=True, blank=True)`
- `carga/models.py:1057` — `que FojaDeMedicion.anterior_items_map())."""`
- `carga/models.py:1242` — `fojaitem_foja = models.ForeignKey("FojaDeMedicion", verbose_name="Foja de Medición", on_delete=models.CASCADE, related_name="items")`
- `carga/models.py:1275` — `fotofoja_foja = models.ForeignKey("FojaDeMedicion", verbose_name="Foja de Medición", on_delete=models.CASCADE, related_name="fotos")`
- `carga/signals.py:3` — `from .models import FojaDeMedicion, FojaDeMedicionItem, PlanDeTrabajosEtapa, ContratoMonto, ContratoTramoPago`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
