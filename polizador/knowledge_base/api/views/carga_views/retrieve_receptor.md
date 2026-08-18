---
symbol: retrieve_receptor
kind: function
module: api/views/carga_views.py
lines: 92-93
signature_hash: sha1:9dbb5777bcf79a4ced47e576c79c9eed57d03c1d
authored: true
---

# retrieve_receptor

**Módulo:** `api/views/carga_views.py` (líneas 92-93)

## Propósito

Devuelve un `Receptor` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_receptor(request, id: int):
```

## Uso real

`GET /v1/api/receptore/{{id}}/` — response=`ReceptorOut`.

## Ver también

- [Receptor](../../../carga/models/Receptor.md)
