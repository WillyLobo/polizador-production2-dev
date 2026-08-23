---
symbol: retrieve_region
kind: function
module: api/views/carga_views.py
lines: 408-409
signature_hash: sha1:e04af9789f8a7b86d167ff6fe318d27ca954ed21
authored: true
---

# retrieve_region

**Módulo:** `api/views/carga_views.py` (líneas 408-409)

## Propósito

Devuelve un `Region` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_region(request, id: int):
```

## Uso real

`GET /v1/api/regione/{{id}}/` — response=`RegionOut`.

## Ver también

- [Region](../../../carga/models/Region.md)
