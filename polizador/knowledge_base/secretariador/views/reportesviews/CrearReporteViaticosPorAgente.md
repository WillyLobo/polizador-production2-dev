---
symbol: CrearReporteViaticosPorAgente
kind: class
module: secretariador/views/reportesviews.py
lines: 27-86
signature_hash: sha1:192218a368de67d763a361fa5333f9efc000c1ac
authored: true
---

# CrearReporteViaticosPorAgente

**Módulo:** `secretariador/views/reportesviews.py` (líneas 27-86) · hereda de `PermissionRequiredMixin, generic.ListView`

## Propósito

Reporte de viáticos totales por Agente en un rango de fechas (últimos 30 días por defecto): itera **todos** los Agentes y para cada uno agrega/suma sus `ComisionadoSolicitud` (de Solicitud directa o de Incorporación) en el rango — un patrón N+1 real (una query de agregación por Agente, no una sola query agrupada por agente), aceptable mientras el padrón de Agentes no sea grande.

## Firma

```python
class CrearReporteViaticosPorAgente(PermissionRequiredMixin, generic.ListView):
```

## Uso real

`CrearReporteViaticosPorAgente` (`secretariador:crear-reporte-viaticos-por-agente`), enlazada desde el mega-menú "Reportes".

## Ver también

- [ComisionadoSolicitud](../../models/ComisionadoSolicitud.md)
