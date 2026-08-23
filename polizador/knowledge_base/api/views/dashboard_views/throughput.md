---
symbol: throughput
kind: function
module: api/views/dashboard_views.py
lines: 18-25
signature_hash: sha1:bf900569d35c8bfb1aa2a21757d21af82a97295e
authored: true
---

# throughput

**Módulo:** `api/views/dashboard_views.py` (líneas 18-25)

## Propósito

Serie temporal de creación de registros por modelo trackeado de una app (`core.dashboard_data.record_throughput`), para los gráficos del dashboard — 404 si `app_label` no está en `TRACKED_MODELS`.

## Firma

```python
def throughput(request, app_label: str):
```

## Uso real

`GET /v1/api/dashboard/throughput/{app_label}/` — consumido por `DashboardView` (`core/views.py`) vía JS (Chart.js).

## Ver también

- [DashboardView](../../../core/views/DashboardView.md)
