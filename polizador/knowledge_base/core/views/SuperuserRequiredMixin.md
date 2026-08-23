---
symbol: SuperuserRequiredMixin
kind: class
module: core/views.py
lines: 22-24
signature_hash: sha1:686d40b80fb7b871c7d357336cc8ef91cc90171e
authored: true
---

# SuperuserRequiredMixin

**Módulo:** `core/views.py` (líneas 22-24) · hereda de `LoginRequiredMixin, UserPassesTestMixin`

## Propósito

El mixin de permisos de toda página `/administracion/*`: `LoginRequiredMixin` + `UserPassesTestMixin` con `test_func` comprobando `request.user.is_superuser`. Todas las vistas de este archivo lo usan — es el patrón estándar del proyecto para "solo superusers" (ver CLAUDE.md).

## Firma

```python
class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
```

## Uso real

`class DashboardView(SuperuserRequiredMixin, TemplateView)`, y toda otra vista de `core/views.py`.

## Ver también

- [DashboardView](DashboardView.md)
- [KnowledgeBaseIndexView](KnowledgeBaseIndexView.md)
