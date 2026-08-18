---
symbol: Aseguradora
kind: class
module: carga/models.py
lines: 119-133
signature_hash: sha1:12a514aeaf1df7aa0e63b87e0241cc582c4b212c
authored: false
---

# Aseguradora

**Módulo:** `carga/models.py` (líneas 119-133)

## Propósito

_(pendiente de autoría)_

## Firma

```python
class Aseguradora(models.Model):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `carga/models.py:180` — `poliza_aseguradora = models.ForeignKey("Aseguradora", verbose_name="Aseguradora", on_delete=models.CASCADE)`
- `carga/views/aseguradoraviews.py:7` — `from carga.models import Aseguradora`
- `carga/views/aseguradoraviews.py:15` — `model = Aseguradora`
- `carga/views/aseguradoraviews.py:24` — `model = Aseguradora`
- `carga/views/aseguradoraviews.py:30` — `title = "Crear Aseguradora"`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
