---
symbol: _invalidar_texto_incorporacion
kind: function
module: secretariador/signals.py
lines: 70-71
signature_hash: sha1:f067fe861e7d87c0a666e8bbec43dd3499c093e4
authored: true
---

# _invalidar_texto_incorporacion

**Módulo:** `secretariador/signals.py` (líneas 70-71)

## Propósito

Wrapper de una línea sobre [_invalidar_texto](_invalidar_texto.md) fijado a
`Incorporacion`/`incorporacion_texto_actuacion` — la contraparte de
[_invalidar_texto_solicitud](_invalidar_texto_solicitud.md) para el otro modelo con texto
editable a mano.

## Firma

```python
def _invalidar_texto_incorporacion(incorporacion_id):
```

## Uso real

Llamado directamente desde
[invalidar_texto_actuacion_por_comisionados](invalidar_texto_actuacion_por_comisionados.md)
cuando el `ComisionadoSolicitud` que cambió es de la propia Incorporacion
(`comisionadosolicitud_incorporacion_foreign_id`), y desde
[_invalidar_incorporacion_de_solicitud](_invalidar_incorporacion_de_solicitud.md) cuando lo
que cambió fue la Solicitud asociada.

## Ver también

- [_invalidar_texto](_invalidar_texto.md)
- [_invalidar_incorporacion_de_solicitud](_invalidar_incorporacion_de_solicitud.md)
- [Incorporacion](../models/Incorporacion.md)
