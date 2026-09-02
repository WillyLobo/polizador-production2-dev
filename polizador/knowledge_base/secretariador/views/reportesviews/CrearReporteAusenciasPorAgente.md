---
symbol: CrearReporteAusenciasPorAgente
kind: class
module: secretariador/views/reportesviews.py
lines: 207-265
signature_hash: sha1:d2b3cf2961e2409af0d5ab97a0709c394816d711
authored: true
---
# CrearReporteAusenciasPorAgente

**Módulo:** `secretariador/views/reportesviews.py` (líneas 207-265) · hereda de `PermissionRequiredMixin, generic.ListView`

## Propósito

Reporte de días en comisión (ausencias) por Agente en un rango de fechas, con el detalle de fechas concretas (`solicitud_fechas()`/`incorporacion_solicitud.solicitud_fechas()`) concatenadas en una sola columna de texto.

## Firma

```python
class CrearReporteAusenciasPorAgente(PermissionRequiredMixin, generic.ListView):
```

## Uso real

`CrearReporteAusenciasPorAgente` (`secretariador:crear-reporte-ausencias-por-agente`).

## Ver también

- [ComisionadoSolicitud](../../models/ComisionadoSolicitud.md)