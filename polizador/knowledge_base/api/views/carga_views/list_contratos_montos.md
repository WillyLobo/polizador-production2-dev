---
symbol: list_contratos_montos
kind: function
module: api/views/carga_views.py
lines: 1652-1656
signature_hash: sha1:a837c509bad75708f5f207a71435fc32ba6aab41
authored: true
---

# list_contratos_montos

**Módulo:** `api/views/carga_views.py` (líneas 1652-1656)

## Propósito

Listado paginado (`PerPagePagination`) de `ContratoMonto`, gateado por `require_model_perm(ContratoMonto)` (permiso `view_<modelo>`). Con `?contrato=` para acotar a un Contrato. Sin endpoint `retrieve` — el consumidor solo necesita listar/crear/editar/borrar, nunca pedir uno suelto.

## Firma

```python
def list_contratos_montos(request, contrato: str=''):
```

## Uso real

`GET /v1/api/contratos-montos/` — response=`List[ContratoMontoOut]`.

## Ver también

- [ContratoMonto](../../../carga/models/ContratoMonto.md)
