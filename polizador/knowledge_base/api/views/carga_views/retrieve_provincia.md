---
symbol: retrieve_provincia
kind: function
module: api/views/carga_views.py
lines: 371-372
signature_hash: sha1:f46d42116c23f906832238f807c9381e52487414
authored: true
---

# retrieve_provincia

**Módulo:** `api/views/carga_views.py` (líneas 371-372)

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
