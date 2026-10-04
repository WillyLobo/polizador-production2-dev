---
symbol: DashboardView
kind: class
module: core/views.py
lines: 58-77
signature_hash: sha1:4617b057572a2506887015ab00effa4fb7df34a5
authored: true
---
# DashboardView

**Módulo:** `core/views.py` (líneas 58-77) · hereda de `SuperuserRequiredMixin, TemplateView`

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