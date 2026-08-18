---
symbol: _generar_solicitud_docx
kind: function
module: secretariador/views/solicitudviews.py
lines: 100-125
signature_hash: sha1:2fc64a467736020d0c0dcf036bbdcffffadf94c7
authored: true
---

# _generar_solicitud_docx

**Módulo:** `secretariador/views/solicitudviews.py` (líneas 100-125)

## Propósito

Genera el `.docx` final: si la Solicitud ya tiene `solicitud_texto_actuacion` guardado (editado a mano), usa esos párrafos/artículos; si no, recalcula con `_calcular_texto_solicitud`. Abre el `EncabezadoDocumento.vigente()` como base y delega el armado real del documento en `docx_builder.build_resolucion_docx` (fuera del alcance de este manifest — combina el encabezado con el texto vía plantilla).

## Firma

```python
def _generar_solicitud_docx(actuacion):
```

## Uso real

`solicitud_docx` (mismo módulo, más abajo).

## Ver también

- [_calcular_texto_solicitud](_calcular_texto_solicitud.md)
- [EncabezadoDocumento](../../models/EncabezadoDocumento.md)
