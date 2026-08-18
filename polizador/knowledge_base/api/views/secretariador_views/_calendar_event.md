---
symbol: _calendar_event
kind: function
module: api/views/secretariador_views.py
lines: 905-913
signature_hash: sha1:b45ec08c4e905a37eb0cf75efcf9841949f74832
authored: true
---

# _calendar_event

**Módulo:** `api/views/secretariador_views.py` (líneas 905-913)

## Propósito

Arma un evento en el formato que espera FullCalendar (`title`/`start`/`end`/`url`/colores) a partir de la Solicitud de origen de un comisionado.

## Firma

```python
def _calendar_event(foreign, title, color=''):
```

## Uso real

`_calendar_events_by_agente`, `calendario_eventos_agente_individual` (mismo módulo).

## Ver también

- [Solicitud](../../../secretariador/models/Solicitud.md)
