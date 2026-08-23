---
symbol: list_contratos_montos
kind: function
module: api/views/carga_views.py
lines: 1631-1635
signature_hash: sha1:3b25be60fbf32c41733b17a443c5ed86c23488ef
authored: true
---

# list_contratos_montos

**Módulo:** `api/views/carga_views.py` (líneas 1631-1635)

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
