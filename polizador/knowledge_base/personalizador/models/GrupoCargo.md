---
symbol: GrupoCargo
kind: class
module: personalizador/models.py
lines: 288-297
signature_hash: sha1:e682fa633a42dc741fa720f11384cb9a43afe52d
authored: true
---

# GrupoCargo

**Módulo:** `personalizador/models.py` (líneas 288-297) · hereda de `models.Model`

## Propósito

Catálogo chico de grupos de cargo (número, `unique`) — usado en `Agente.grupo`.

## Firma

```python
class GrupoCargo(models.Model):
```

## Uso real

`CrearGrupoCargo`/`UpdateGrupoCargo` (`personalizador/views/grupocargoviews.py`).

## Ver también

- [Agente](Agente.md)
