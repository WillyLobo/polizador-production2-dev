---
symbol: _seccion_dashboard
kind: function
module: core/views.py
lines: 63-74
signature_hash: sha1:f2c6e03a1c3ce1011ce74952ec93846f1771b723
authored: false
---

# _seccion_dashboard

**Módulo:** `core/views.py` (líneas 63-74)

## Propósito

_(pendiente de autoría)_

## Firma

```python
def _seccion_dashboard(nombre, funcion, *args):
```

## Uso real

_(pendiente de autoría — candidatos detectados automáticamente:)_

- `core/views.py:86` — `"changes": _seccion_dashboard(f"cambios de {app_label}", dashboard_data.changes_feed, app_label),`
- `core/views.py:92` — `context["login_summary"] = _seccion_dashboard("resumen de logins", dashboard_data.login_summary)`
- `core/views.py:93` — `context["recent_logins"] = _seccion_dashboard("últimos logins", dashboard_data.recent_logins)`
- `core/views.py:94` — `context["db_health"] = _seccion_dashboard("estado de la base", dashboard_data.db_health)`
- `core/views.py:95` — `context["db_performance"] = _seccion_dashboard("consultas costosas", dashboard_data.db_performance)`

## Flujo de datos

_(pendiente de autoría)_

## Ver también

_(pendiente de autoría)_
