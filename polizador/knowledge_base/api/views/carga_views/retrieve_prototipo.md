---
symbol: retrieve_prototipo
kind: function
module: api/views/carga_views.py
lines: 1161-1162
signature_hash: sha1:5f5e3fb603d611c28e366147a85f5a55a766e134
authored: true
---

# retrieve_prototipo

**Módulo:** `api/views/carga_views.py` (líneas 1161-1162)

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
