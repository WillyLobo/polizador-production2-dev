---
symbol: list_uvi
kind: function
module: api/views/carga_views.py
lines: 1727-1728
signature_hash: sha1:34a5980a858ea51a25c852d2bba90db486986b67
authored: true
---

# list_uvi

**Módulo:** `api/views/carga_views.py` (líneas 1727-1728)

## Propósito

Listado paginado (`PerPagePagination`) de `Uvi`, gateado por `require_model_perm(Uvi)` (permiso `view_<modelo>`). Sin `retrieve` genérico — ver `latest_uvi` para el caso de uso real ("la cotización vigente").

## Firma

```python
def list_uvi(request):
```

## Uso real

`GET /v1/api/uvi/` — response=`List[UviOut]`.

## Ver también

- [Uvi](../../../carga/models/Uvi.md)
