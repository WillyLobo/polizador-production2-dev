---
symbol: latest_indec
kind: function
module: api/views/carga_views.py
lines: 1773-1777
signature_hash: sha1:9269a622196ca60c59733963f94defb682fd0bbf
authored: true
---

# latest_indec

**Módulo:** `api/views/carga_views.py` (líneas 1773-1777)

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
