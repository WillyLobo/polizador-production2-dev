---
symbol: _sin_plantilla
kind: function
module: carga/views/textoresolucionviews.py
lines: 194-201
signature_hash: sha1:62b10fa8f217716b99477db157488fccf614659d
authored: true
---

# _sin_plantilla

**Módulo:** `carga/views/textoresolucionviews.py` (líneas 194-201)

## Propósito

Pantalla "no hay texto base para este alcance" (`textoresolucion/sin-texto-resolucion.html`),
con el link para crear la plantilla que ya lleva este certificado como muestra. Responde
**409**, no 404: el certificado existe y lo que falta es la plantilla.

## Firma

```python
def _sin_plantilla(request, certificado):
```

## Uso real

Lo devuelven [editar_texto_resolucion_certificado](editar_texto_resolucion_certificado.md) y [resolucion_certificado_docx](resolucion_certificado_docx.md) cuando `_texto_certificado` no encuentra snapshot ni plantilla.

## Ver también

- [CrearTextoResolucion](CrearTextoResolucion.md)
