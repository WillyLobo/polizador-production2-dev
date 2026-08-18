---
symbol: GrupoCargo
kind: class
module: personalizador/models.py
lines: 249-258
signature_hash: sha1:82df07385e23ad06c6efec38188a130c71ea1c81
authored: true
---

# GrupoCargo

**Módulo:** `personalizador/models.py` (líneas 249-258) · hereda de `models.Model`

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
