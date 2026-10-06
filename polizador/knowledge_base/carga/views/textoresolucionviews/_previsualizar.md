---
symbol: _previsualizar
kind: function
module: carga/views/textoresolucionviews.py
lines: 25-39
signature_hash: sha1:76211a5baa3759e4f7024aa50f3477ad1c2c6855
authored: true
---

# _previsualizar

**Módulo:** `carga/views/textoresolucionviews.py` (líneas 25-39)

## Propósito

Renderiza los bloques de una plantilla contra un certificado de muestra para el panel de
vista previa del editor. Devuelve `(bloques_renderizados, faltantes, error)` y **nunca
lanza**: un `TextoResolucionError` (Jinja inválido) o cualquier otra excepción (datos
incompletos del certificado de muestra) vuelve como `error`, para mostrarlo junto al texto
en vez de un 500. Los bloques se devuelven ya numerados (`numerar_articulos`), igual que
saldrían en el `.docx`. Sin certificado devuelve `(None, set(), None)`.

## Firma

```python
def _previsualizar(bloques, certificado):
```

## Uso real

```python
# carga/views/textoresolucionviews.py (TextoResolucionEditorMixin.get_context_data)
preview, faltantes, error = _previsualizar(bloques, certificado)
```

## Ver también

- [TextoResolucionEditorMixin](TextoResolucionEditorMixin.md)
