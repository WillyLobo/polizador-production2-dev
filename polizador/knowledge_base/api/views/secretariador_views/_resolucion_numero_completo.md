---
symbol: _resolucion_numero_completo
kind: function
module: api/views/secretariador_views.py
lines: 315-320
signature_hash: sha1:0adcb4a8359dcf1f039935416637c3e5c9fded3b
authored: true
---

# _resolucion_numero_completo

**Módulo:** `api/views/secretariador_views.py` (líneas 315-320)

## Propósito

Arma el número mostrado de una Resolución: `"numero/ano"` para Presidencia, `"numero/acta/ano"` para Directorio (con acta) — usado en la columna del listado combinado Presidencia+Directorio, donde `InstrumentosLegalesResoluciones.__str__` no alcanza porque ahí el formato es "RES-...".

## Firma

```python
def _resolucion_numero_completo(r: InstrumentosLegalesResoluciones) -> str:
```

## Uso real

`_resolucion_datatable_row` (mismo módulo, más abajo).

## Ver también

- [InstrumentosLegalesResoluciones](../../../secretariador/models/InstrumentosLegalesResoluciones.md)
