---
symbol: retrieve_conjunto
kind: function
module: api/views/carga_views.py
lines: 1481-1482
signature_hash: sha1:f89fda13f89b40dae4b0856f4517419485bf1a35
authored: true
---

# retrieve_conjunto

**Módulo:** `api/views/carga_views.py` (líneas 1481-1482)

## Propósito

Devuelve un `ConjuntoLicitado` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_conjunto(request, id: int):
```

## Uso real

`GET /v1/api/conjunto/{{id}}/` — response=`ConjuntoLicitadoOut`.

## Ver también

- [ConjuntoLicitado](../../../carga/models/ConjuntoLicitado.md)
