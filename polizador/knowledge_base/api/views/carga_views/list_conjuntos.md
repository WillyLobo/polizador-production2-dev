---
symbol: list_conjuntos
kind: function
module: api/views/carga_views.py
lines: 1475-1476
signature_hash: sha1:5845ea5b40c56a06a0d38bbe6030bf64572409b6
authored: true
---

# list_conjuntos

**Módulo:** `api/views/carga_views.py` (líneas 1475-1476)

## Propósito

Listado paginado (`PerPagePagination`) de `ConjuntoLicitado`, gateado por `require_model_perm(ConjuntoLicitado)` (permiso `view_<modelo>`).

## Firma

```python
def list_conjuntos(request):
```

## Uso real

`GET /v1/api/conjuntos/` — response=`List[ConjuntoLicitadoOut]`.

## Ver también

- [ConjuntoLicitado](../../../carga/models/ConjuntoLicitado.md)
