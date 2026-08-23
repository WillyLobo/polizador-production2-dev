---
symbol: list_solicitudes
kind: function
module: api/views/secretariador_views.py
lines: 587-591
signature_hash: sha1:d3e3daedf239a4a430a453ebfae5290df49a4e1d
authored: true
---

# list_solicitudes

**Módulo:** `api/views/secretariador_views.py` (líneas 587-591)

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
