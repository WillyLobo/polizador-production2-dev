---
symbol: Programa
kind: class
module: carga/models.py
lines: 213-227
signature_hash: sha1:596422f29fba99dc532fa4a67bfb113afbe27043
authored: true
---

# Programa

**Módulo:** `carga/models.py` (líneas 213-227) · hereda de `models.Model`

## Propósito

Catálogo de programas de financiamiento (ej. FO.PRO.VI., PROCREAR) bajo los que se ejecuta una Obra — ver `Obra.obra_programa`.

## Firma

```python
class Programa(models.Model):
```

## Uso real

Alta/edición vía `ProgramaForm` (`carga/forms/programaforms.py`).

## Ver también

- [Obra](Obra.md)
