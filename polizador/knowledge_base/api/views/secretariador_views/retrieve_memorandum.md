---
symbol: retrieve_memorandum
kind: function
module: api/views/secretariador_views.py
lines: 63-64
signature_hash: sha1:fb0b3a6e8d30c343854efc19313657643ca72f13
authored: true
---

# retrieve_memorandum

**Módulo:** `api/views/secretariador_views.py` (líneas 63-64)

## Propósito

Devuelve un `InstrumentosLegalesMemorandum` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_memorandum(request, id: int):
```

## Uso real

`GET /v1/api/memorandum/{{id}}/` — response=`InstrumentosLegalesMemorandumOut`.

## Ver también

- [InstrumentosLegalesMemorandum](../../../secretariador/models/InstrumentosLegalesMemorandum.md)
