---
symbol: list_indec
kind: function
module: api/views/carga_views.py
lines: 1767-1768
signature_hash: sha1:d03b27d1f236853dc0a34655cbf417333fdba69b
authored: true
---

# list_indec

**Módulo:** `api/views/carga_views.py` (líneas 1767-1768)

## Propósito

Listado paginado (`PerPagePagination`) de `INDEC`, gateado por `require_model_perm(INDEC)` (permiso `view_<modelo>`). Mismo patrón que Uvi: ver `latest_indec`.

## Firma

```python
def list_indec(request):
```

## Uso real

`GET /v1/api/indec/` — response=`List[INDECOut]`.

## Ver también

- [INDEC](../../../carga/models/INDEC.md)
