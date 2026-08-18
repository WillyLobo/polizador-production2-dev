---
symbol: retrieve_municipio
kind: function
module: api/views/carga_views.py
lines: 532-533
signature_hash: sha1:d471b2646bdeae2da9e5446c69146f7adc68925a
authored: true
---

# retrieve_municipio

**Módulo:** `api/views/carga_views.py` (líneas 532-533)

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
