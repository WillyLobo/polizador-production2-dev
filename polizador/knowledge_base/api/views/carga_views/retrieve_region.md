---
symbol: retrieve_region
kind: function
module: api/views/carga_views.py
lines: 409-410
signature_hash: sha1:9c5c825c3b700225a5732cd4b091949f1d3a043a
authored: true
---

# retrieve_region

**Módulo:** `api/views/carga_views.py` (líneas 409-410)

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
