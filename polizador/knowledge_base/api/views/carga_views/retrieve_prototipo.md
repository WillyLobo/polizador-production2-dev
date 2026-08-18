---
symbol: retrieve_prototipo
kind: function
module: api/views/carga_views.py
lines: 1160-1161
signature_hash: sha1:811617544c70cfa0a9ebbc9088bc8534d22fbd1e
authored: true
---

# retrieve_prototipo

**Módulo:** `api/views/carga_views.py` (líneas 1160-1161)

## Propósito

Devuelve un `Prototipo` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_prototipo(request, id: int):
```

## Uso real

`GET /v1/api/prototipo/{{id}}/` — response=`PrototipoOut`.

## Ver también

- [Prototipo](../../../carga/models/Prototipo.md)
