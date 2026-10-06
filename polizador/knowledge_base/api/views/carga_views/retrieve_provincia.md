---
symbol: retrieve_provincia
kind: function
module: api/views/carga_views.py
lines: 372-373
signature_hash: sha1:d824058c9a7000c83fe6ef004263c223d782d087
authored: true
---

# retrieve_provincia

**Módulo:** `api/views/carga_views.py` (líneas 372-373)

## Propósito

Devuelve un `Provincia` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_provincia(request, id: int):
```

## Uso real

`GET /v1/api/provincia/{{id}}/` — response=`ProvinciaOut`.

## Ver también

- [Provincia](../../../carga/models/Provincia.md)
