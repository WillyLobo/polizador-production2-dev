---
symbol: list_conjuntos
kind: function
module: api/views/carga_views.py
lines: 1474-1475
signature_hash: sha1:f4e5e2c76fa5bf7f07ec3d70408672c84e5b1811
authored: true
---

# list_conjuntos

**Módulo:** `api/views/carga_views.py` (líneas 1474-1475)

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
