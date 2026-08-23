---
symbol: generate_name_memorandum
kind: function
module: secretariador/models.py
lines: 50-64
signature_hash: sha1:61b5459bc4bfb0c76a6078fc9cc6cfcfec610e87
authored: true
---

# generate_name_memorandum

**Módulo:** `secretariador/models.py` (líneas 50-64)

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
