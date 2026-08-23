---
symbol: solicitud_docx
kind: function
module: secretariador/views/solicitudviews.py
lines: 147-154
signature_hash: sha1:1397f149b3c18a836ac22cecf255e9f23deb8cc3
authored: true
---

# solicitud_docx

**Módulo:** `secretariador/views/solicitudviews.py` (líneas 147-154)

## Propósito

Descarga el `.docx` generado de una Solicitud, con nombre de archivo igual a su actuación electrónica.

## Firma

```python
def solicitud_docx(request, pk):
```

## Uso real

`solicitud_docx` (`secretariador:crear-documento-solicitud`), destino final del flujo `editar_texto_solicitud` → `revisar_texto_actuacion`.

## Ver también

- [_generar_solicitud_docx](_generar_solicitud_docx.md)
