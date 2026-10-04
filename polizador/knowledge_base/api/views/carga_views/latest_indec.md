---
symbol: latest_indec
kind: function
module: api/views/carga_views.py
lines: 1794-1798
signature_hash: sha1:352ae61dabf84c99edb5ea2b3fea26beb05cd771
authored: true
---

# latest_indec

**Módulo:** `api/views/carga_views.py` (líneas 1794-1798)

## Propósito

Mismo patrón que `latest_uvi`: el registro INDEC más reciente por `mes`.

## Firma

```python
def latest_indec(request):
```

## Uso real

`GET /v1/api/indec-latest/` — response=`INDECOut`.

## Ver también

- [INDEC](../../../carga/models/INDEC.md)
- [latest_uvi](latest_uvi.md)
