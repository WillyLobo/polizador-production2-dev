---
symbol: retrieve_localidad
kind: function
module: api/views/carga_views.py
lines: 616-617
signature_hash: sha1:ed53ba0f8a551272bcfcff061d27ea6ba5809c0e
authored: true
---

# retrieve_localidad

**Módulo:** `api/views/carga_views.py` (líneas 616-617)

## Propósito

Devuelve un `Localidad` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_localidad(request, id: int):
```

## Uso real

`GET /v1/api/localidade/{{id}}/` — response=`LocalidadOut`.

## Ver también

- [Localidad](../../../carga/models/Localidad.md)
