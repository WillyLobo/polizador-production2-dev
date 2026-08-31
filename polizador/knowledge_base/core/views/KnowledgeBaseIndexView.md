---
symbol: KnowledgeBaseIndexView
kind: class
module: core/views.py
lines: 82-92
signature_hash: sha1:cd3c9c1627d88d193a2ad0a4a2940343a9331dba
authored: true
---
# KnowledgeBaseIndexView

**Módulo:** `core/views.py` (líneas 82-92) · hereda de `SuperuserRequiredMixin, TemplateView`

## Propósito

El índice de la Base de Conocimiento (`/administracion/conocimiento/`): carga el árbol completo (`core.knowledge_base.load_tree()`) y cuenta cuántos símbolos están autorados vs. total, para el resumen de progreso que muestra la página.

## Firma

```python
class KnowledgeBaseIndexView(SuperuserRequiredMixin, TemplateView):
```

## Uso real

`KnowledgeBaseIndexView` (`knowledge_base`), enlazada desde el navbar.

## Ver también

- [KnowledgeBasePageView](KnowledgeBasePageView.md)