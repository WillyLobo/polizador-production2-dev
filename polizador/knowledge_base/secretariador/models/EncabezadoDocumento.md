---
symbol: EncabezadoDocumento
kind: class
module: secretariador/models.py
lines: 655-681
signature_hash: sha1:7eff83b2bb80b9697d7e58b9e18a8864d1b99f06
authored: true
---
# EncabezadoDocumento

**Módulo:** `secretariador/models.py` (líneas 655-681) · hereda de `models.Model`

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