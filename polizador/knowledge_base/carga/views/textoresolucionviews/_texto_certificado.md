---
symbol: _texto_certificado
kind: function
module: carga/views/textoresolucionviews.py
lines: 170-191
signature_hash: sha1:530eae304f0d215c31d3b9cdcdc4beb49f67b0f5
authored: true
---

# _texto_certificado

**Módulo:** `carga/views/textoresolucionviews.py` (líneas 170-191)

## Propósito

Decide qué texto corresponde a un Certificado concreto. Devuelve
`(bloques, faltantes, plantilla, error)`:
- Si el certificado tiene un snapshot editado a mano (`certificado_texto_resolucion` con
  `bloques`), lo usa tal cual (ya está renderizado) con `plantilla=None`.
- Si no, busca la plantilla del alcance (`TextoResolucionCertificado.para_certificado`) y
  la renderiza contra `contexto_certificado()`, reportando las variables sin resolver. Un
  `TextoResolucionError` vuelve como `error`.
- Sin snapshot ni plantilla devuelve `(None, set(), None, None)`, y quien llama muestra
  [_sin_plantilla](_sin_plantilla.md).

## Firma

```python
def _texto_certificado(certificado):
```

## Uso real

Punto de entrada común de [editar_texto_resolucion_certificado](editar_texto_resolucion_certificado.md) y [resolucion_certificado_docx](resolucion_certificado_docx.md).

## Ver también

- [TextoResolucionCertificado](../../models/TextoResolucionCertificado.md)
- [Certificado](../../models/Certificado.md)
