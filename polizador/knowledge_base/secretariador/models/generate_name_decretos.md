---
symbol: generate_name_decretos
kind: function
module: secretariador/models.py
lines: 18-32
signature_hash: sha1:a6a37eea7db8ba6d5cd0e364654d754a77d0c7dc
authored: true
---

# generate_name_decretos

**Módulo:** `secretariador/models.py` (líneas 18-32)

## Propósito

Callback `upload_to` para el PDF de un `InstrumentosLegalesDecretos`: `instrumentoslegales/decretos/<numero>-<ano>-<tipo>.pdf` — a diferencia de los `upload_to` de `carga` (que usan un UUID), acá el nombre de archivo es humano-legible (número-año-tipo), sin partición por fecha en subdirectorios.

## Firma

```python
def generate_name_decretos(instance, filename):
```

## Uso real

`InstrumentosLegalesDecretos.instrumentolegaldecretos` (mismo módulo, más abajo).

## Ver también

- [InstrumentosLegalesDecretos](InstrumentosLegalesDecretos.md)
