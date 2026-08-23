---
symbol: list_incorporaciones
kind: function
module: api/views/secretariador_views.py
lines: 820-824
signature_hash: sha1:ed6d3e556ecf1ea09c12bf3f32c66cbb95e2052f
authored: true
---

# list_incorporaciones

**Módulo:** `api/views/secretariador_views.py` (líneas 820-824)

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
