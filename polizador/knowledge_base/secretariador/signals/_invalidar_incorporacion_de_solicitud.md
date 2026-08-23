---
symbol: _invalidar_incorporacion_de_solicitud
kind: function
module: secretariador/signals.py
lines: 74-80
signature_hash: sha1:de528274e4b4a4506dde5f87884de9488182ac71
authored: true
---

# _invalidar_incorporacion_de_solicitud

**Módulo:** `secretariador/signals.py` (líneas 74-80)

## Propósito

Puente entre `Solicitud` e `Incorporacion`: `_calcular_texto_incorporacion`
(`incorporacionviews.py`) arma el texto de una Incorporacion leyendo datos de
`actuacion.incorporacion_solicitud` (resolución, fechas, tareas, localidades, agentes
originales) además de los propios de la Incorporacion. Eso significa que un cambio en la
Solicitud "padre" puede dejar desactualizado el `incorporacion_texto_actuacion` guardado
de su Incorporacion, aunque la Incorporacion en sí no haya cambiado nada.

Esta función resuelve la Incorporacion asociada a `solicitud_id` — a lo sumo una, por el
`UniqueConstraint` `unique_incorporacion_1` sobre `incorporacion_solicitud` — y delega la
invalidación en [_invalidar_texto_incorporacion](_invalidar_texto_incorporacion.md). Si la
Solicitud no tiene Incorporacion asociada, `Incorporacion.objects.filter(...).first()`
devuelve `None` y `_invalidar_texto_incorporacion(None)` no hace nada (ver el `if not pk`
de [_invalidar_texto](_invalidar_texto.md)) — no hace falta chequear existencia antes de
llamarla.

## Firma

```python
def _invalidar_incorporacion_de_solicitud(solicitud_id):
```

## Uso real

Llamada desde los tres puntos que invalidan el texto de la propia Solicitud, para
propagar la invalidación a su Incorporacion si tiene una:
[invalidar_texto_actuacion_por_cambio_de_datos](invalidar_texto_actuacion_por_cambio_de_datos.md)
(campos propios de la Solicitud que también alimentan el texto de la Incorporacion, ver
`CAMPOS_INCORPORACION_DESDE_SOLICITUD`),
[invalidar_texto_actuacion_por_localidades](invalidar_texto_actuacion_por_localidades.md) y
[invalidar_texto_actuacion_por_comisionados](invalidar_texto_actuacion_por_comisionados.md).

## Ver también

- [_invalidar_texto_incorporacion](_invalidar_texto_incorporacion.md)
- [Solicitud](../models/Solicitud.md)
- [Incorporacion](../models/Incorporacion.md)
