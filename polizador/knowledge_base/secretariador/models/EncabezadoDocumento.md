---
symbol: EncabezadoDocumento
kind: class
module: secretariador/models.py
lines: 644-670
signature_hash: sha1:8ef455e2f5a43efe2f5e9e0ee78ca1637aff4e52
authored: true
---

# EncabezadoDocumento

**Módulo:** `secretariador/models.py` (líneas 644-670) · hereda de `models.Model`

## Propósito

El archivo `.docx` base (con el encabezado institucional de primera página ya configurado en Word) sobre el que se generan todas las resoluciones/incorporaciones — `docx_builder.build_resolucion_docx` parte de este archivo y le inserta el texto calculado. `vigente()` devuelve siempre el subido más recientemente; no hay versión activa/inactiva explícita, subir uno nuevo reemplaza al vigente para todo generado de ahí en más.

## Firma

```python
class EncabezadoDocumento(models.Model):
```

## Uso real

`ActualizarEncabezado` (`secretariador/views/encabezadoviews.py`); `EncabezadoDocumento.vigente()` se llama al generar cualquier `.docx` (`solicitudviews`, `solicitud_exteriorviews`, `incorporacionviews`).

## Ver también

- [Solicitud](Solicitud.md)
- [Incorporacion](Incorporacion.md)
