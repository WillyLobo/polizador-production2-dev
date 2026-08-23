---
symbol: retrieve_localidad
kind: function
module: api/views/carga_views.py
lines: 615-616
signature_hash: sha1:4e1ac476999e515edc3b18c68068d60667858bdd
authored: true
---

# retrieve_localidad

**Módulo:** `api/views/carga_views.py` (líneas 615-616)

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
