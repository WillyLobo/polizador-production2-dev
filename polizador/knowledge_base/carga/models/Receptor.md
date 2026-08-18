---
symbol: Receptor
kind: class
module: carga/models.py
lines: 87-101
signature_hash: sha1:0be9de63e1a1a029945f42a96e885dbb4da5fdb1
authored: true
---

# Receptor

**Módulo:** `carga/models.py` (líneas 87-101) · hereda de `models.Model`

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
