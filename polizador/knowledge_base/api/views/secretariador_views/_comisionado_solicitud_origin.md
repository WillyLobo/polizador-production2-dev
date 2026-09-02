---
symbol: _comisionado_solicitud_origin
kind: function
module: api/views/secretariador_views.py
lines: 906-909
signature_hash: sha1:0936a96cf89bedb89ad7a6a11666527ce54c8e8d
authored: true
---
# _comisionado_solicitud_origin

**Módulo:** `api/views/secretariador_views.py` (líneas 906-909)

## Propósito

Mismo patrón que `ComisionadoSolicitud.get_origin()` (modelo): resuelve si el origen de un comisionado es una `Solicitud` directa o la `Solicitud` de una `Incorporacion` — reimplementado acá en vez de llamar al método del modelo (redundancia menor entre capa API y modelo).

## Firma

```python
def _comisionado_solicitud_origin(comisionado):
```

## Uso real

`_calendar_events_by_agente`, `calendario_eventos_agente_individual` (mismo módulo).

## Ver también

- [ComisionadoSolicitud](../../../secretariador/models/ComisionadoSolicitud.md)