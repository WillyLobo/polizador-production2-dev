---
symbol: list_comisionados_solicitudes
kind: function
module: api/views/secretariador_views.py
lines: 796-800
signature_hash: sha1:3bae7eaf591a1e598161fd0180b102d1b3b7b4c8
authored: true
---

# list_comisionados_solicitudes

**Módulo:** `api/views/secretariador_views.py` (líneas 796-800)

## Propósito

Listado paginado (`PerPagePagination`) de `ComisionadoSolicitud`, gateado por `require_model_perm(ComisionadoSolicitud)` (permiso `view_<modelo>`). Con `?solicitud=` para acotar. Requiere además el grupo `dirgral_usuarios`. Sin `retrieve`/`update`.

## Firma

```python
def list_comisionados_solicitudes(request, solicitud: str=''):
```

## Uso real

`GET /v1/api/comisionados-solicitudes/` — response=`List[ComisionadoSolicitudOut]`.

## Ver también

- [ComisionadoSolicitud](../../../secretariador/models/ComisionadoSolicitud.md)
