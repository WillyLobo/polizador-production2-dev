---
symbol: _calendar_events_by_agente
kind: function
module: api/views/secretariador_views.py
lines: 916-927
signature_hash: sha1:5ca63f806054e00bd58647f64a96e97a424433bf
authored: true
---

# _calendar_events_by_agente

**Módulo:** `api/views/secretariador_views.py` (líneas 916-927)

## Propósito

Arma la lista de eventos para el calendario general (anual/semanal, no el individual): marca en rojo (`color="red"`) la segunda comisión (o posterior) de un mismo agente que empieza el mismo día — una señal visual de posible superposición/error de carga, calculada con un `set` de `(nombre, fecha_desde)` ya vistos.

## Firma

```python
def _calendar_events_by_agente(comisionados):
```

## Uso real

`calendario_eventos_anual`, `calendario_eventos_semanal` (mismo módulo).

## Ver también

- [_calendar_event](_calendar_event.md)
- [CrearReporteComisionesDuplicadas](../../../secretariador/views/reportesviews/CrearReporteComisionesDuplicadas.md) — mismo espíritu de detección de superposición, por otro camino.
