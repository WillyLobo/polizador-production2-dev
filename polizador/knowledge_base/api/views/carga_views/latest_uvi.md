---
symbol: latest_uvi
kind: function
module: api/views/carga_views.py
lines: 1733-1737
signature_hash: sha1:87c79f365afa594e4faa419f06806824a4c04392
authored: true
---

# latest_uvi

**Módulo:** `api/views/carga_views.py` (líneas 1733-1737)

## Propósito

Devuelve la cotización de Uvi más reciente (`order_by('-uvi_fecha').first()`); 404 si la tabla está vacía. Reemplaza a `retrieve_uvi` para el caso de uso real: casi nadie pide un Uvi por `id`, se pide "el vigente".

## Firma

```python
def latest_uvi(request):
```

## Uso real

`GET /v1/api/uvi-latest/` — response=`UviOut`.

## Ver también

- [Uvi](../../../carga/models/Uvi.md)
