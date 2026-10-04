---
symbol: list_contratos_digitales
kind: function
module: api/views/carga_views.py
lines: 1717-1718
signature_hash: sha1:5d34d7e5466fff7429c2d2735e66be3feda03866
authored: true
---

# list_contratos_digitales

**Módulo:** `api/views/carga_views.py` (líneas 1717-1718)

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
