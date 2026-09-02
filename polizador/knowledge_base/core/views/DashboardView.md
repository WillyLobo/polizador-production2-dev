---
symbol: DashboardView
kind: class
module: core/views.py
lines: 35-54
signature_hash: sha1:8ce41238898a302b44b325cdd14179a6107dd3a9
authored: true
---
# DashboardView

**Módulo:** `core/views.py` (líneas 35-54) · hereda de `SuperuserRequiredMixin, TemplateView`

## Propósito

El panel principal de `/administracion/dashboard/`: arma, por cada app trackeada (`core.dashboard_data.TRACKED_MODELS`, fuera del alcance de este manifest), un feed de cambios recientes por modelo, más resumen de logins, salud de Sentry, salud/performance de la base — toda la lógica de agregación vive en `dashboard_data.py`, esta vista solo la invoca y arma el contexto.

## Firma

```python
class DashboardView(SuperuserRequiredMixin, TemplateView):
```

## Uso real

`DashboardView` (`dashboard`), enlazada desde el navbar ("Administracion > Dashboard").

## Ver también

- [LoginEvent](../models/LoginEvent.md)