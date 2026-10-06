---
symbol: generate_name_memorandum
kind: function
module: secretariador/models.py
lines: 51-65
signature_hash: sha1:2aa8547ff954e898ba9c6eefae0dfc55078d4f25
authored: true
---

# generate_name_memorandum

**Módulo:** `secretariador/models.py` (líneas 51-65)

## Propósito

Mismo patrón para Memorandums: `instrumentoslegales/memorandum/<numero>-<ano>-<tipo>.pdf`.

## Firma

```python
def generate_name_memorandum(instance, filename):
```

## Uso real

`InstrumentosLegalesMemorandum.instrumentolegalmemorandum` (mismo módulo, más abajo).

## Ver también

- [InstrumentosLegalesMemorandum](InstrumentosLegalesMemorandum.md)
