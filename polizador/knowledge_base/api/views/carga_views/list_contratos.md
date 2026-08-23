---
symbol: list_contratos
kind: function
module: api/views/carga_views.py
lines: 1591-1595
signature_hash: sha1:b25604dd0b8ca07806fb76f1fd5be69cc5b2e8a4
authored: true
---

# list_contratos

**Módulo:** `api/views/carga_views.py` (líneas 1591-1595)

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
