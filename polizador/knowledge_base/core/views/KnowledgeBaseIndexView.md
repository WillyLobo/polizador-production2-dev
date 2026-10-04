---
symbol: KnowledgeBaseIndexView
kind: class
module: core/views.py
lines: 105-115
signature_hash: sha1:a329f10dcef06ccac89f83f809e95c2187d488e8
authored: true
---
# KnowledgeBaseIndexView

**Módulo:** `core/views.py` (líneas 105-115) · hereda de `SuperuserRequiredMixin, TemplateView`

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