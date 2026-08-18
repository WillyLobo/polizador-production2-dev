---
symbol: _calcular_texto_incorporacion
kind: function
module: secretariador/views/incorporacionviews.py
lines: 19-86
signature_hash: sha1:a0adb032c011b43d1860b4275c3e878e0a54ed9f
authored: true
---

# _calcular_texto_incorporacion

**Módulo:** `secretariador/views/incorporacionviews.py` (líneas 19-86)

## Propósito

Igual que `solicitudviews._calcular_texto_solicitud` pero para incorporar agentes a una Solicitud ya resuelta: menciona tanto los agentes de la Solicitud original (`agentes_solicitud`) como los recién incorporados (`agentes_incorporacion`) — dos listas separadas en la redacción, no una combinada.

## Firma

```python
def _calcular_texto_incorporacion(actuacion):
```

## Uso real

`_generar_incorporacion_docx` (mismo módulo).

## Ver también

- [Incorporacion](../../models/Incorporacion.md)
- [_calcular_texto_solicitud](../solicitudviews/_calcular_texto_solicitud.md)
