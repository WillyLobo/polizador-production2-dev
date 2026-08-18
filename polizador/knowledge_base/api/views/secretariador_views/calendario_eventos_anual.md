---
symbol: calendario_eventos_anual
kind: function
module: api/views/secretariador_views.py
lines: 950-956
signature_hash: sha1:8587ff85b03bf8c6095f167a011988288d5d2df4
authored: true
---

# calendario_eventos_anual

**Módulo:** `api/views/secretariador_views.py` (líneas 950-956)

## Propósito

Eventos del calendario general de todo un año — usa `_calendar_events_by_agente` (con la marca en rojo de superposiciones).

## Firma

```python
def calendario_eventos_anual(request, ano: int):
```

## Uso real

`GET /v1/api/calendario/anual/?ano=<ano>` — consumido por `CalendarioAnual` (`secretariador/views/reportesviews.py`).

## Ver también

- [CalendarioAnual](../../../secretariador/views/reportesviews/CalendarioAnual.md)
- [_calendar_events_by_agente](_calendar_events_by_agente.md)
