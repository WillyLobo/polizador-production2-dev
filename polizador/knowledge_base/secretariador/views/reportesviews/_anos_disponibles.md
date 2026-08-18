---
symbol: _anos_disponibles
kind: function
module: secretariador/views/reportesviews.py
lines: 15-18
signature_hash: sha1:de98046a16061c5153575abcfb86e63d728c0978
authored: true
---

# _anos_disponibles

**Módulo:** `secretariador/views/reportesviews.py` (líneas 15-18)

## Propósito

Años con al menos una Solicitud (`Solicitud.objects.dates("solicitud_fecha_desde", "year")`), para poblar los `<select name="ano">` de los reportes de calendario en vez de hardcodear un rango fijo.

## Firma

```python
def _anos_disponibles():
```

## Uso real

`CrearReporteViaticosPorAgenteIndividual.get_context_data`, `CalendarioAnual.get_context_data` (mismo módulo).

## Ver también

- [Solicitud](../../models/Solicitud.md)
