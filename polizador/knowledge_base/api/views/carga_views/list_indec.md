---
symbol: list_indec
kind: function
module: api/views/carga_views.py
lines: 1788-1789
signature_hash: sha1:9cb2c6c2c7a022db4131dab27350b85d3e308635
authored: true
---

# list_indec

**Módulo:** `api/views/carga_views.py` (líneas 1788-1789)

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
