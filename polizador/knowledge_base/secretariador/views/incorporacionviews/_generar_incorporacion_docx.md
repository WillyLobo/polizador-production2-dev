---
symbol: _generar_incorporacion_docx
kind: function
module: secretariador/views/incorporacionviews.py
lines: 89-114
signature_hash: sha1:a7030f95d82f834f8335b45c53a5f57b76562a79
authored: true
---

# _generar_incorporacion_docx

**Módulo:** `secretariador/views/incorporacionviews.py` (líneas 89-114)

## Propósito

Mismo patrón que `_generar_solicitud_docx`/`_generar_exterior_docx` para Incorporaciones.

## Firma

```python
def _generar_incorporacion_docx(actuacion):
```

## Uso real

`incorporacion_docx` (mismo módulo, más abajo).

## Ver también

- [_calcular_texto_incorporacion](_calcular_texto_incorporacion.md)
- [_generar_solicitud_docx](../solicitudviews/_generar_solicitud_docx.md) — mismo patrón, con la nota sobre invalidación del texto guardado.
- [invalidar_texto_incorporacion_por_cambio_de_datos](../../signals/invalidar_texto_incorporacion_por_cambio_de_datos.md)
