---
symbol: Area
kind: class
module: carga/models.py
lines: 111-125
signature_hash: sha1:61f302b826768fe63072c4c34d8ca838deecb408
authored: true
---

# Area

**Módulo:** `carga/models.py` (líneas 111-125) · hereda de `models.Model`

## Propósito

Catálogo de áreas/oficinas internas por las que circula una Póliza — ver `Poliza_Movimiento.poliza_movimiento_area`. Tabla de referencia simple.

## Firma

```python
class Area(models.Model):
```

## Uso real

Alta/edición vía `AreaForm` (`carga/forms/areaforms.py`).

## Ver también

- [Poliza_Movimiento](Poliza_Movimiento.md) — único FK hacia este modelo.
