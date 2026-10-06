---
symbol: list_provincias
kind: function
module: api/views/carga_views.py
lines: 366-367
signature_hash: sha1:f4af946aa2949129334c6a2162484f34ec6a8301
authored: true
---

# list_provincias

**Módulo:** `api/views/carga_views.py` (líneas 366-367)

## Propósito

Listado paginado (`PerPagePagination`) de `Provincia`, gateado por `require_model_perm(Provincia)` (permiso `view_<modelo>`).

## Firma

```python
def list_provincias(request):
```

## Uso real

`GET /v1/api/provincias/` — response=`List[ProvinciaOut]`.

## Ver también

- [Provincia](../../../carga/models/Provincia.md)
