---
symbol: CrearReporteViaticosporArea
kind: class
module: secretariador/views/reportesviews.py
lines: 89-204
signature_hash: sha1:6109847d4a70539678625fa56595ee855fc52b79
authored: true
---
# CrearReporteViaticosporArea

**Módulo:** `secretariador/views/reportesviews.py` (líneas 89-204) · hereda de `PermissionRequiredMixin, generic.ListView`

## Propósito

Mismo patrón que `CrearReporteViaticosPorAgente`, pero agrupado por el Agente **solicitante** (`solicitud_solicitante`, el área que pidió la comisión) en vez del comisionado — mismo N+1 por agente.

## Firma

```python
class CrearReporteViaticosporArea(PermissionRequiredMixin, generic.ListView):
```

## Uso real

`CrearReporteViaticosporArea` (`secretariador:crear-reporte-viaticos-por-area`).

## Ver también

- [CrearReporteViaticosPorAgente](CrearReporteViaticosPorAgente.md)