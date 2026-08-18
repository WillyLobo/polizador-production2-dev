---
symbol: list_gerencias
kind: function
module: api/views/personalizador_views.py
lines: 56-57
signature_hash: sha1:a07db3301ff2ca242bce105a4efc944d90562242
authored: true
---

# list_gerencias

**Módulo:** `api/views/personalizador_views.py` (líneas 56-57)

## Propósito

Listado paginado (`PerPagePagination`) de `Gerencia`, gateado por `require_model_perm(Gerencia)` (permiso `view_<modelo>`). Sin `retrieve`/`update` — de solo lectura salvo alta/baja desde esta API (la edición pasa por la UI de Django, no por este endpoint).

## Firma

```python
def list_gerencias(request):
```

## Uso real

`GET /v1/api/gerencias/` — response=`List[GerenciaOut]`.

## Ver también

- [Gerencia](../../../personalizador/models/Gerencia.md)
