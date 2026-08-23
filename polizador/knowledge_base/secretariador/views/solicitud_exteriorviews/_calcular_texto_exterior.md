---
symbol: _calcular_texto_exterior
kind: function
module: secretariador/views/solicitud_exteriorviews.py
lines: 21-103
signature_hash: sha1:e0daa3288a80aab8fab7f91209f78387ccda62cb
authored: true
---

# _calcular_texto_exterior

**Módulo:** `secretariador/views/solicitud_exteriorviews.py` (líneas 21-103)

## Propósito

Igual que `solicitudviews._calcular_texto_solicitud` pero con la redacción usada para Solicitudes fuera de la Provincia del Chaco: menciona la provincia/ciudad de destino, distingue traslado aéreo (sin mención de vehículo) de terrestre, y ajusta singular/plural ("al agente"/"a los agentes") de forma más explícita que la versión Chaco.

## Firma

```python
def _calcular_texto_exterior(actuacion):
```

## Uso real

`_generar_exterior_docx` (mismo módulo).

## Ver también

- [Solicitud](../../models/Solicitud.md)
- [_calcular_texto_solicitud](../solicitudviews/_calcular_texto_solicitud.md) — la contraparte para Solicitudes dentro del Chaco.
