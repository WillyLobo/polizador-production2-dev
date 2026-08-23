---
symbol: ApartadoCargo
kind: class
module: personalizador/models.py
lines: 227-236
signature_hash: sha1:04f2877ff234c5a69607f6a83a81979162f1c67d
authored: true
---

# ApartadoCargo

**Módulo:** `personalizador/models.py` (líneas 227-236) · hereda de `models.Model`

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
