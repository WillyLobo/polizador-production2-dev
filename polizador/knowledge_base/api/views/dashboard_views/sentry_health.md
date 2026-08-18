---
symbol: sentry_health
kind: function
module: api/views/dashboard_views.py
lines: 30-38
signature_hash: sha1:55ab532d0cc7e678f89c8c69d3ba23310fe8582e
authored: true
---

# sentry_health

**Módulo:** `api/views/dashboard_views.py` (líneas 30-38)

## Propósito

Estado de errores sin resolver en Sentry (`core.dashboard_data.sentry_health()`) — devuelve `{configured: false}` sin tocar la API de Sentry si no hay credenciales configuradas, en vez de fallar.

## Firma

```python
def sentry_health(request):
```

## Uso real

`GET /v1/api/dashboard/sentry/` — consumido por `DashboardView`.

## Ver también

- [DashboardView](../../../core/views/DashboardView.md)
