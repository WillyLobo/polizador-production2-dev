---
symbol: KnowledgeBasePageView
kind: class
module: core/views.py
lines: 91-114
signature_hash: sha1:1a1517f461c3be87d66c6af761bd477a0aac8a6f
authored: true
---

# KnowledgeBasePageView

**Módulo:** `core/views.py` (líneas 91-114) · hereda de `SuperuserRequiredMixin, TemplateView`

## Propósito

La página de un símbolo puntual de la Base de Conocimiento. Resuelve `page_path` contra el manifest vía `resolve_page_path` (whitelist anti path-traversal — nunca construye un `Path` a partir del `page_path` crudo de la URL), 404 si no es conocido; si el `.html` pre-renderizado existe, lo lee y reescribe sus links (`_rewrite_doc_links`) antes de pasarlo al template.

## Firma

```python
class KnowledgeBasePageView(SuperuserRequiredMixin, TemplateView):
```

## Uso real

`KnowledgeBasePageView` (`knowledge_base_page`), destino de cada link del árbol/index.

## Ver también

- [_rewrite_doc_links](_rewrite_doc_links.md)
- [KnowledgeBaseIndexView](KnowledgeBaseIndexView.md)
