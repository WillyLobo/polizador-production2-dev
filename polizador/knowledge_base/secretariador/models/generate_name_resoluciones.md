---
symbol: generate_name_resoluciones
kind: function
module: secretariador/models.py
lines: 33-50
signature_hash: sha1:0e3651b5c41fe1583c1e88064e63279865c67bd2
authored: true
---

# generate_name_resoluciones

**Módulo:** `secretariador/models.py` (líneas 33-50)

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
