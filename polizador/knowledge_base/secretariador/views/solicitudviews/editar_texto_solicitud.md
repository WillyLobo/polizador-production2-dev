---
symbol: editar_texto_solicitud
kind: function
module: secretariador/views/solicitudviews.py
lines: 130-142
signature_hash: sha1:c20dae1ef142b6f3f56e9b4b12d667a1d1a2937b
authored: true
---

# editar_texto_solicitud

**Módulo:** `secretariador/views/solicitudviews.py` (líneas 130-142)

## Propósito

Punto de entrada del flujo "revisar antes de generar" para una Solicitud dentro del Chaco: calcula el texto por defecto y delega en `revisar_texto_actuacion` (compartida entre los tres flujos).

## Firma

```python
def editar_texto_solicitud(request, pk):
```

## Uso real

`editar_texto_solicitud` (`secretariador:editar-texto-solicitud`), enlazada desde la ficha de Solicitud.

## Ver también

- [revisar_texto_actuacion](../textoactuacionviews/revisar_texto_actuacion.md)
