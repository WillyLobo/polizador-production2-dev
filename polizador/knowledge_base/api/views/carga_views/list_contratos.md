---
symbol: list_contratos
kind: function
module: api/views/carga_views.py
lines: 1592-1596
signature_hash: sha1:a807540b789aec3765a1964ecce5979c8ef14365
authored: true
---

# list_contratos

**Módulo:** `api/views/carga_views.py` (líneas 1592-1596)

## Propósito

Listado paginado (`PerPagePagination`) de `Contrato`, gateado por `require_model_perm(Contrato)` (permiso `view_<modelo>`). Con `?obra=` para acotar a una Obra.

## Firma

```python
def list_contratos(request, obra: str=''):
```

## Uso real

`GET /v1/api/contratos/` — response=`List[ContratoOut]`.

## Ver también

- [Contrato](../../../carga/models/Contrato.md)
