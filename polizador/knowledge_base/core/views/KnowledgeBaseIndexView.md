---
symbol: KnowledgeBaseIndexView
kind: class
module: core/views.py
lines: 78-88
signature_hash: sha1:13c995f8e01d2e04ca027f83b2c97b2ccb4e9558
authored: true
---

# KnowledgeBaseIndexView

**Módulo:** `core/views.py` (líneas 78-88) · hereda de `SuperuserRequiredMixin, TemplateView`

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
