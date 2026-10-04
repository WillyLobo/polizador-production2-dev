---
symbol: latest_uvi
kind: function
module: api/views/carga_views.py
lines: 1754-1758
signature_hash: sha1:2120ee2a6b38f2cf52552a3ba93059e83a21108f
authored: true
---

# latest_uvi

**Módulo:** `api/views/carga_views.py` (líneas 1754-1758)

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
