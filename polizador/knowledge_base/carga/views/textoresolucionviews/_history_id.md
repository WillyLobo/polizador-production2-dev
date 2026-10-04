---
symbol: _history_id
kind: function
module: carga/views/textoresolucionviews.py
lines: 243-249
signature_hash: sha1:67b2d0d07dd31310664a2b3d5a2e1ef4113534d1
authored: true
---

# _history_id

**Módulo:** `carga/views/textoresolucionviews.py` (líneas 243-249)

## Propósito

Id de la fila más reciente de `textoresolucion_history` de una plantilla, que es su
versión vigente. Se guarda en el snapshot del certificado para poder auditar con qué
versión del texto base se emitió una resolución, aunque la plantilla se haya editado
después. Devuelve `None` sin plantilla (snapshot re-guardado) o sin historial.

## Firma

```python
def _history_id(plantilla):
```

## Uso real

```python
# carga/views/textoresolucionviews.py (editar_texto_resolucion_certificado)
"textoresolucion_history_id": _history_id(plantilla),
```

## Ver también

- [editar_texto_resolucion_certificado](editar_texto_resolucion_certificado.md)
- [TextoResolucionCertificado](../../models/TextoResolucionCertificado.md)
