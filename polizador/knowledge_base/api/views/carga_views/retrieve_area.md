---
symbol: retrieve_area
kind: function
module: api/views/carga_views.py
lines: 129-130
signature_hash: sha1:a3a44c1f0d6994382b71b7b1a68d3eb4999c2679
authored: true
---

# retrieve_area

**Módulo:** `api/views/carga_views.py` (líneas 129-130)

## Propósito

Devuelve un `Area` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_area(request, id: int):
```

## Uso real

`GET /v1/api/area/{{id}}/` — response=`AreaOut`.

## Ver también

- [Area](../../../carga/models/Area.md)
