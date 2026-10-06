---
symbol: Receptor
kind: class
module: carga/models.py
lines: 95-109
signature_hash: sha1:03a38de2142f7eea926a3675c3981643393070ae
authored: true
---

# Receptor

**Módulo:** `carga/models.py` (líneas 95-109) · hereda de `models.Model`

## Propósito

Catálogo de personas/entidades que reciben una Póliza al moverse entre áreas — ver `Poliza_Movimiento.poliza_movimiento_receptor`. Tabla de referencia simple, sin lógica propia.

## Firma

```python
class Receptor(models.Model):
```

## Uso real

Alta/edición vía `ReceptorForm` (`carga/forms/receptorforms.py`), un `ModelForm` estándar sin campos calculados.

## Ver también

- [Poliza_Movimiento](Poliza_Movimiento.md) — único FK hacia este modelo.
