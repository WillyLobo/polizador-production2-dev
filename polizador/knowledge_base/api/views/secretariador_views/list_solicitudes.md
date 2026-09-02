---
symbol: list_solicitudes
kind: function
module: api/views/secretariador_views.py
lines: 594-598
signature_hash: sha1:dd432b36061c0a04d13b5bc0dbac195dd0e6f833
authored: true
---
# list_solicitudes

**Módulo:** `api/views/secretariador_views.py` (líneas 594-598)

## Propósito

Listado paginado (`PerPagePagination`) de `Solicitud`, gateado por `require_model_perm(Solicitud)` (permiso `view_<modelo>`). Con `?provincia=` para acotar. Sin `update` genérico (la edición pasa por las vistas Django, no por esta API).

## Firma

```python
def list_solicitudes(request, provincia: str=''):
```

## Uso real

`GET /v1/api/solicitudes/` — response=`List[SolicitudOut]`.

## Ver también

- [Solicitud](../../../secretariador/models/Solicitud.md)