---
symbol: Programa
kind: class
module: carga/models.py
lines: 298-312
signature_hash: sha1:0f36e5c4e57e20b0589871cca2023b23d6cbe68a
authored: true
---

# Programa

**Módulo:** `carga/models.py` (líneas 298-312) · hereda de `models.Model`

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
