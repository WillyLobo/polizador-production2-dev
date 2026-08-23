---
symbol: list_contratos_digitales
kind: function
module: api/views/carga_views.py
lines: 1696-1697
signature_hash: sha1:48e2f1ddaf893c207aa4e4dc492b11f90e99b2e0
authored: true
---

# list_contratos_digitales

**Módulo:** `api/views/carga_views.py` (líneas 1696-1697)

## Propósito

Listado paginado (`PerPagePagination`) de `ContratosDigitales`, gateado por `require_model_perm(ContratosDigitales)` (permiso `view_<modelo>`). Sin endpoint `retrieve`.

## Firma

```python
def list_contratos_digitales(request):
```

## Uso real

`GET /v1/api/contratos-digitales/` — response=`List[ContratosDigitalesOut]`.

## Ver también

- [ContratosDigitales](../../../carga/models/ContratosDigitales.md)
