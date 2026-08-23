---
symbol: Area
kind: class
module: carga/models.py
lines: 103-117
signature_hash: sha1:39dc53cc3d5be8027ae84f64985b0acee5134e7b
authored: true
---

# Area

**Módulo:** `carga/models.py` (líneas 103-117) · hereda de `models.Model`

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
