---
symbol: CrearReporteViaticosporArea
kind: class
module: secretariador/views/reportesviews.py
lines: 89-151
signature_hash: sha1:47cc8e3fac3fef0b6332b2cbc96932e868a46ff3
authored: true
---

# CrearReporteViaticosporArea

**Módulo:** `secretariador/views/reportesviews.py` (líneas 89-151) · hereda de `PermissionRequiredMixin, generic.ListView`

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
