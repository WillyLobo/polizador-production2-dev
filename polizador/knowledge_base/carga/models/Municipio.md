---
symbol: Municipio
kind: class
module: carga/models.py
lines: 297-313
signature_hash: sha1:d3cb8abcf1a118aef8254eb5359fbc82805109dd
authored: false
---

# Municipio

**Módulo:** `carga/models.py` (líneas 297-313)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class Municipio(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:287` — `localidad_municipio     = models.ForeignKey("Municipio", verbose_name="Municipio", on_delete=models.CASCADE)`
- `carga/models.py:343` — `obra_municipio_m = models.ManyToManyField("Municipio", related_name="obra_municipio", verbose_name="Municipio", blank=True)`
- `carga/views/municipioviews.py:7` — `from carga.models import Municipio`
- `carga/views/municipioviews.py:15` — `model = Municipio`
- `carga/views/municipioviews.py:24` — `model = Municipio`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
