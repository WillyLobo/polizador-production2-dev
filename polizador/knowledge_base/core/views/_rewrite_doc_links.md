---
symbol: _rewrite_doc_links
kind: function
module: core/views.py
lines: 67-79
signature_hash: sha1:13eaef14dd596c0ce2f0f435590ee0116678ea93
authored: true
---
# _rewrite_doc_links

**Módulo:** `core/views.py` (líneas 67-79)

## Propósito

Reescribe, en tiempo de request, los links relativos `../modulo/Simbolo.md` que un `.md`
autorado usa en su sección "Ver también" (formato pensado para navegar el markdown crudo
en un PR/GitHub) a la URL real `knowledge_base_page` — resuelve la ruta relativa contra el
directorio del `page_path` actual con `posixpath.normpath(posixpath.join(...))`, y arma el
href final con `reverse()`. Deliberadamente vive acá (capa de vista) y no en
`core/knowledge_base.py` (que solo convierte Markdown a HTML sin saber nada de URLs de
Django) — separación explícita entre "generar HTML" y "servir HTML con links reales"
documentada en el propio plan de implementación de esta feature.

## Firma

```python
def _rewrite_doc_links(html: str, page_path: str) -> str:
```

## Uso real

`KnowledgeBasePageView.get_context_data` (mismo módulo, más abajo).

## Ver también

- [KnowledgeBasePageView](KnowledgeBasePageView.md)