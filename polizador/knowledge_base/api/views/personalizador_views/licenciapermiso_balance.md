---
symbol: licenciapermiso_balance
kind: function
module: api/views/personalizador_views.py
lines: 912-925
signature_hash: sha1:fb565efc0ccb888dfdeaf4ad2f5c7bd7707be4d6
authored: true
---

# licenciapermiso_balance

**Módulo:** `api/views/personalizador_views.py` (líneas 912-925)

## Propósito

Días/horas correspondientes, usados y disponibles de un `TipoLicenciaPermiso` para un `Agente` en un año dado (actual por defecto) — expone `personalizador.licencias.balance_tipo` como endpoint HTTP, el mismo cálculo que usa `ControlLicenciasAgente` (`personalizador/views/licenciapermisoviews.py`) del lado servidor-renderizado; acá es para consumo AJAX/JS (ej. actualizar un balance sin recargar la página al elegir tipo/año en un `<select>`).

## Firma

```python
def licenciapermiso_balance(request, agente: int, tipo: int, anio: int=None):
```

## Uso real

`GET /v1/api/licenciapermiso-balance/?agente=<id>&tipo=<id>&anio=<anio>` — response=`LicenciaPermisoBalanceOut`.

## Ver también

- [LicenciaPermiso](../../../personalizador/models/LicenciaPermiso.md)
- [ControlLicenciasAgente](../../../personalizador/views/licenciapermisoviews/ControlLicenciasAgente.md)
