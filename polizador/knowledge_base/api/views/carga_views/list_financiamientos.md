---
symbol: list_financiamientos
kind: function
module: api/views/carga_views.py
lines: 1228-1229
signature_hash: sha1:e278b8fb502f11c7dade80dcfac5e3c02a2e5efa
authored: true
---

# list_financiamientos

**Módulo:** `api/views/carga_views.py` (líneas 1228-1229)

## Propósito

Listado paginado (`PerPagePagination`) de `CertificadoFinanciamiento`, gateado por `require_model_perm(CertificadoFinanciamiento)` (permiso `view_<modelo>`).

## Firma

```python
def list_financiamientos(request):
```

## Uso real

`GET /v1/api/financiamientos/` — response=`List[CertificadoFinanciamientoOut]`.

## Ver también

- [CertificadoFinanciamiento](../../../carga/models/CertificadoFinanciamiento.md)
