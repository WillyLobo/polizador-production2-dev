---
symbol: calendario_eventos_agente_individual
kind: function
module: api/views/secretariador_views.py
lines: 932-945
signature_hash: sha1:438cc2eda933aecd5b971788b37a32286a695b10
authored: true
---

# calendario_eventos_agente_individual

**Módulo:** `api/views/secretariador_views.py` (líneas 932-945)

## Propósito

Eventos del calendario de un Agente puntual en un año dado (Solicitudes directas + Incorporaciones, excluyendo anuladas) — sin la lógica de "marcar en rojo" de `_calendar_events_by_agente` (acá el título de cada evento es la actuación, no el nombre del agente, porque ya se sabe de quién es el calendario).

## Firma

```python
def calendario_eventos_agente_individual(request, agente: int, ano: int):
```

## Uso real

`GET /v1/api/calendario/agente-individual/?agente=<id>&ano=<ano>` — consumido por `CrearReporteViaticosPorAgenteIndividual` (`secretariador/views/reportesviews.py`).

## Ver también

- [CrearReporteViaticosPorAgenteIndividual](../../../secretariador/views/reportesviews/CrearReporteViaticosPorAgenteIndividual.md)
- [_comisionado_solicitud_origin](_comisionado_solicitud_origin.md)
