---
symbol: list_polizas
kind: function
module: api/views/carga_views.py
lines: 1807-1810
signature_hash: sha1:7c06560374005b29fb263951cb489465fff03e1b
authored: true
---

# list_polizas

**Módulo:** `api/views/carga_views.py` (líneas 1807-1810)

## Propósito

Listado paginado (`PerPagePagination`) de `Poliza`, gateado por `require_model_perm(Poliza)` (permiso `view_<modelo>`).

## Firma

```python
def list_polizas(request):
```

## Uso real

`GET /v1/api/polizas/` — response=`List[PolizaOut]`.

## Ver también

- [Poliza](../../../carga/models/Poliza.md)
