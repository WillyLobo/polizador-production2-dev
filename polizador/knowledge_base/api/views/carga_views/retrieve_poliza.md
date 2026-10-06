---
symbol: retrieve_poliza
kind: function
module: api/views/carga_views.py
lines: 1836-1840
signature_hash: sha1:d1ac3802597b398693c43dfcc8a6b28439dbfb8b
authored: true
---

# retrieve_poliza

**Módulo:** `api/views/carga_views.py` (líneas 1836-1840)

## Propósito

Devuelve un `Poliza` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_poliza(request, id: int):
```

## Uso real

`GET /v1/api/poliza/{{id}}/` — response=`PolizaOut`.

## Ver también

- [Poliza](../../../carga/models/Poliza.md)
