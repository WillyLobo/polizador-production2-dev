---
symbol: retrieve_conjunto
kind: function
module: api/views/carga_views.py
lines: 1480-1481
signature_hash: sha1:80a2d14e03fee89a411064d86a9c37e783786ab9
authored: true
---

# retrieve_conjunto

**Módulo:** `api/views/carga_views.py` (líneas 1480-1481)

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
