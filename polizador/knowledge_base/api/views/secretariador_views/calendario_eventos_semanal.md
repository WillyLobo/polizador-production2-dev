---
symbol: calendario_eventos_semanal
kind: function
module: api/views/secretariador_views.py
lines: 961-972
signature_hash: sha1:226e6ca2d1f8bb5fe66fc0eb29de83c3122fb6a9
authored: true
---

# calendario_eventos_semanal

**Módulo:** `api/views/secretariador_views.py` (líneas 961-972)

## Propósito

Eventos de las próximas dos semanas (hoy hasta 13 días después, calculado desde el lunes de esta semana), opcionalmente acotado a un Agente (`?agente=`).

## Firma

```python
def calendario_eventos_semanal(request, agente: Optional[int]=None):
```

## Uso real

`GET /v1/api/calendario/semanal/` — consumido por `CalendarioSemanal` (`secretariador/views/reportesviews.py`).

## Ver también

- [CalendarioSemanal](../../../secretariador/views/reportesviews/CalendarioSemanal.md)
- [_calendar_events_by_agente](_calendar_events_by_agente.md)
