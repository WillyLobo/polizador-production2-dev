---
symbol: retrieve_decreto
kind: function
module: api/views/secretariador_views.py
lines: 175-176
signature_hash: sha1:f0d2110b2795a0beaba9609b2669f76c0a48da8b
authored: true
---

# retrieve_decreto

**Módulo:** `api/views/secretariador_views.py` (líneas 175-176)

## Propósito

Devuelve un `InstrumentosLegalesDecretos` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_decreto(request, id: int):
```

## Uso real

`GET /v1/api/decreto/{{id}}/` — response=`InstrumentosLegalesDecretosOut`.

## Ver también

- [InstrumentosLegalesDecretos](../../../secretariador/models/InstrumentosLegalesDecretos.md)
