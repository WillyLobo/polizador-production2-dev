---
symbol: list_financiamientos
kind: function
module: api/views/carga_views.py
lines: 1229-1230
signature_hash: sha1:753709d603eeb7b95779b1141a250b5c5f595663
authored: true
---

# list_financiamientos

**Módulo:** `api/views/carga_views.py` (líneas 1229-1230)

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
