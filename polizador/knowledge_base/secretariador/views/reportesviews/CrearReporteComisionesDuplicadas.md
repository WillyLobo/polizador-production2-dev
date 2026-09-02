---
symbol: CrearReporteComisionesDuplicadas
kind: class
module: secretariador/views/reportesviews.py
lines: 268-343
signature_hash: sha1:d350e1866d07e1f276712c610b01a81747492e7a
authored: true
---
# CrearReporteComisionesDuplicadas

**Módulo:** `secretariador/views/reportesviews.py` (líneas 268-343) · hereda de `PermissionRequiredMixin, generic.ListView`

## Propósito

Detecta Solicitudes que comparten exactamente las mismas fechas y localidades (posible carga duplicada por error) — agrupa por la tupla `(fechas, localidades)` y reporta los grupos con más de un elemento. Recorre día por día del rango en vez de una sola query agrupada, re-consultando `Solicitud.objects.filter(solicitud_fecha_desde=fecha)` en cada iteración del loop de fechas.

## Firma

```python
class CrearReporteComisionesDuplicadas(PermissionRequiredMixin, generic.ListView):
```

## Uso real

`CrearReporteComisionesDuplicadas` (`secretariador:crear-reporte-duplicados`).

## Ver también

- [Solicitud](../../models/Solicitud.md)