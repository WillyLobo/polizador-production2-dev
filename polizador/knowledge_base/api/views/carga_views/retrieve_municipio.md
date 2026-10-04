---
symbol: retrieve_municipio
kind: function
module: api/views/carga_views.py
lines: 533-534
signature_hash: sha1:18223a6b8d8c02ae8214923f8e6fac2e05387204
authored: true
---

# retrieve_municipio

**Módulo:** `api/views/carga_views.py` (líneas 533-534)

## Propósito

Devuelve un `Municipio` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_municipio(request, id: int):
```

## Uso real

`GET /v1/api/municipio/{{id}}/` — response=`MunicipioOut`.

## Ver también

- [Municipio](../../../carga/models/Municipio.md)
