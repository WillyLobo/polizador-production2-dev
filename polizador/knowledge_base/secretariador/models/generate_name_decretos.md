---
symbol: generate_name_decretos
kind: function
module: secretariador/models.py
lines: 17-31
signature_hash: sha1:d2b52324ae4b00e2f5232a6811c76a9100606159
authored: true
---

# generate_name_decretos

**Módulo:** `secretariador/models.py` (líneas 17-31)

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
