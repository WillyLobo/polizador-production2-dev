---
symbol: list_comisionados_solicitudes
kind: function
module: api/views/secretariador_views.py
lines: 803-807
signature_hash: sha1:0a2a11d622fb7bbe0bb813076d3da2f6b0963c58
authored: true
---
# list_comisionados_solicitudes

**Módulo:** `api/views/secretariador_views.py` (líneas 803-807)

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