---
symbol: resolucion_certificado_docx
kind: function
module: carga/views/textoresolucionviews.py
lines: 254-281
signature_hash: sha1:247d1a7a290edf1c4b0109673f614f266c5af178
authored: true
---

# resolucion_certificado_docx

**Módulo:** `carga/views/textoresolucionviews.py` (líneas 254-281)

## Propósito

Descarga el `.docx` de la resolución de un Certificado
(`resolucion-certificado-<expediente>.docx`, con `/` reemplazadas por `-`), armado con
`carga.resolucion_docx.build_resolucion_certificado(bloques)`. Antes de generar el
documento:
- sin snapshot ni plantilla → [_sin_plantilla](_sin_plantilla.md) (409);
- error de render → 500 con el mensaje;
- **variables sin resolver** → no emite nada: deja un `messages.error` con la lista y
  redirige a la pantalla de revisión. Una resolución se firma, y emitirla con un
  `«falta: ...»` adentro es peor que no emitirla.

Un `ResolucionDocxError` también vuelve como 500 con mensaje. Exige
`carga.view_certificado`.

## Firma

```python
def resolucion_certificado_docx(request, pk):
```

## Uso real

`carga:resolucion-certificado-docx`. También es el destino por defecto después de guardar en `editar_texto_resolucion_certificado`.

## Ver también

- [_texto_certificado](_texto_certificado.md)
- [editar_texto_resolucion_certificado](editar_texto_resolucion_certificado.md)
