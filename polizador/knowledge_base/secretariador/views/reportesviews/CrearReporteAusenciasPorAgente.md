---
symbol: CrearReporteAusenciasPorAgente
kind: class
module: secretariador/views/reportesviews.py
lines: 154-212
signature_hash: sha1:3158ad280e6fe147f53ed2f468b7ddaeae0344ed
authored: true
---

# CrearReporteAusenciasPorAgente

**Módulo:** `secretariador/views/reportesviews.py` (líneas 154-212) · hereda de `PermissionRequiredMixin, generic.ListView`

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
