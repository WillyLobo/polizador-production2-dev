---
symbol: retrieve_poliza
kind: function
module: api/views/carga_views.py
lines: 1815-1819
signature_hash: sha1:734fd37a638fb4428d96bae2cf1027d1f4dbdf74
authored: true
---

# retrieve_poliza

**Módulo:** `api/views/carga_views.py` (líneas 1815-1819)

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
