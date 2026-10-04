---
symbol: retrieve_area
kind: function
module: api/views/carga_views.py
lines: 130-131
signature_hash: sha1:e109126505728a023fd05b63cdedbfd4007d9a2d
authored: true
---

# retrieve_area

**Módulo:** `api/views/carga_views.py` (líneas 130-131)

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
