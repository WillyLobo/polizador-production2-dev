---
symbol: ApartadoCargo
kind: class
module: personalizador/models.py
lines: 266-275
signature_hash: sha1:c69915725d98d5c79a77bf54bbd65e3242c4ab7d
authored: true
---

# ApartadoCargo

**Módulo:** `personalizador/models.py` (líneas 266-275) · hereda de `models.Model`

## Propósito

Catálogo chico (un carácter, `unique`) de "apartados" de cargo — usado en `Agente.apartado`.

## Firma

```python
class ApartadoCargo(models.Model):
```

## Uso real

`CrearApartadoCargo`/`UpdateApartadoCargo` (`personalizador/views/apartadocargoviews.py`).

## Ver también

- [Agente](Agente.md)
