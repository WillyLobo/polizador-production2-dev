---
symbol: _generar_exterior_docx
kind: function
module: secretariador/views/solicitud_exteriorviews.py
lines: 106-131
signature_hash: sha1:b98660c8e9e1fc3daf21c0903da5196ff040bf08
authored: true
---

# _generar_exterior_docx

**Módulo:** `secretariador/views/solicitud_exteriorviews.py` (líneas 106-131)

## Propósito

Mismo patrón que `_generar_solicitud_docx`: usa el texto guardado si existe, si no recalcula con `_calcular_texto_exterior`, y delega en `docx_builder.build_resolucion_docx`.

## Firma

```python
def _generar_exterior_docx(actuacion):
```

## Uso real

`exterior_docx` (mismo módulo, más abajo).

## Ver también

- [_calcular_texto_exterior](_calcular_texto_exterior.md)
- [_generar_solicitud_docx](../solicitudviews/_generar_solicitud_docx.md) — mismo patrón, con la nota sobre invalidación del texto guardado.
