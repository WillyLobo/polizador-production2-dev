---
symbol: list_polizas
kind: function
module: api/views/carga_views.py
lines: 1828-1831
signature_hash: sha1:1f6969d5b944fb94b8d4d7335ae010447a757a78
authored: true
---

# list_polizas

**Módulo:** `api/views/carga_views.py` (líneas 1828-1831)

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
