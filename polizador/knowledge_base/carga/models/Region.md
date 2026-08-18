---
symbol: Region
kind: class
module: carga/models.py
lines: 243-256
signature_hash: sha1:581812bfda15800658e0a518d8419f04973d671a
authored: false
---

# Region

**Módulo:** `carga/models.py` (líneas 243-256)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class Region(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:306` — `municipio_region        = models.ForeignKey("Region", verbose_name="Región", on_delete=models.SET_NULL, null=True, blank=True)`
- `carga/models.py:341` — `obra_region = models.ForeignKey("Region", on_delete=models.SET_NULL, verbose_name="Región", null=True, blank=True)`
- `carga/views/regionviews.py:7` — `from carga.models import Region`
- `carga/views/regionviews.py:15` — `model = Region`
- `carga/views/regionviews.py:24` — `model = Region`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
