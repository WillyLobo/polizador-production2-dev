---
symbol: editar_texto_incorporacion
kind: function
module: secretariador/views/incorporacionviews.py
lines: 119-131
signature_hash: sha1:be00b19ab97969943eef497e2efdd12328bc6981
authored: true
---

# editar_texto_incorporacion

**Módulo:** `secretariador/views/incorporacionviews.py` (líneas 119-131)

## Propósito

Punto de entrada del flujo "revisar antes de generar" para una Incorporación, agregando `dia_inhabil` al contexto (tomado de la Solicitud original, no de la Incorporación en sí — una Incorporación no tiene ese campo propio).

## Firma

```python
def editar_texto_incorporacion(request, pk):
```

## Uso real

`editar_texto_incorporacion` (`secretariador:editar-texto-incorporacion`).

## Ver también

- [revisar_texto_actuacion](../textoactuacionviews/revisar_texto_actuacion.md)
