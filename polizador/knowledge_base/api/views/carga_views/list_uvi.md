---
symbol: list_uvi
kind: function
module: api/views/carga_views.py
lines: 1748-1749
signature_hash: sha1:037f7e46a4ba33fb9e8923d876ff12bb6140c639
authored: true
---

# list_uvi

**Módulo:** `api/views/carga_views.py` (líneas 1748-1749)

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
