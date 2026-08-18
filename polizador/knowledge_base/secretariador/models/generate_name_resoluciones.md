---
symbol: generate_name_resoluciones
kind: function
module: secretariador/models.py
lines: 32-49
signature_hash: sha1:9d310800c5aedcfa18bd19ba0bbffe2c68beda04
authored: true
---

# generate_name_resoluciones

**Módulo:** `secretariador/models.py` (líneas 32-49)

## Propósito

Mismo patrón que `generate_name_decretos` para Resoluciones: `instrumentoslegales/resoluciones/<numero>-<acta>-<ano>-<tipo>.pdf` si es de Directorio (lleva acta), o `<numero>-<ano>-<tipo>.pdf` si es de Presidencia.

## Firma

```python
def generate_name_resoluciones(instance, filename):
```

## Uso real

`InstrumentosLegalesResoluciones.instrumentolegalresoluciones` (mismo módulo, más abajo).

## Ver también

- [InstrumentosLegalesResoluciones](InstrumentosLegalesResoluciones.md)
