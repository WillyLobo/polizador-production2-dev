---
symbol: _comisionado_solicitud_origin
kind: function
module: api/views/secretariador_views.py
lines: 899-902
signature_hash: sha1:eef4258e888460fc275cf5d6bbd73418c7322810
authored: true
---

# _comisionado_solicitud_origin

**Módulo:** `api/views/secretariador_views.py` (líneas 899-902)

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
