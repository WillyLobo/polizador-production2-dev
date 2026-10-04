---
symbol: retrieve_receptor
kind: function
module: api/views/carga_views.py
lines: 93-94
signature_hash: sha1:d2c24e32179e15b4ca320bd193596a14518336b3
authored: true
---

# retrieve_receptor

**Módulo:** `api/views/carga_views.py` (líneas 93-94)

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
