---
symbol: calendario_eventos_semanal
kind: function
module: api/views/secretariador_views.py
lines: 968-979
signature_hash: sha1:08f7dd0887fddba703f5c2375c2c3394560613e6
authored: true
---
# calendario_eventos_semanal

**Módulo:** `api/views/secretariador_views.py` (líneas 968-979)

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