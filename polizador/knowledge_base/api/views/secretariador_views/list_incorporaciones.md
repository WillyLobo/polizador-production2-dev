---
symbol: list_incorporaciones
kind: function
module: api/views/secretariador_views.py
lines: 827-831
signature_hash: sha1:07da4a9c82fc935173945f919bd1bbc1a95195b6
authored: true
---
# list_incorporaciones

**Módulo:** `api/views/secretariador_views.py` (líneas 827-831)

## Propósito

Listado paginado (`PerPagePagination`) de `Incorporacion`, gateado por `require_model_perm(Incorporacion)` (permiso `view_<modelo>`). Con `?solicitud=` para acotar. Sin `retrieve`/`update`.

## Firma

```python
def list_incorporaciones(request, solicitud: str=''):
```

## Uso real

`GET /v1/api/incorporaciones/` — response=`List[IncorporacionOut]`.

## Ver también

- [Incorporacion](../../../secretariador/models/Incorporacion.md)