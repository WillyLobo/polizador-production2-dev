---
symbol: list_departamentos_carga
kind: function
module: api/views/carga_views.py
lines: 463-464
signature_hash: sha1:dfa34494c37b3653663363c4757ba7b98ef583d5
authored: true
---

# list_departamentos_carga

**Módulo:** `api/views/carga_views.py` (líneas 463-464)

## Propósito

Listado paginado (`PerPagePagination`) de `Departamento`, gateado por `require_model_perm(Departamento)` (permiso `view_<modelo>`).

## Firma

```python
def list_departamentos_carga(request):
```

## Uso real

`GET /v1/api/departamentos-carga/` — response=`List[DepartamentoOut]`.

## Ver también

- [Departamento](../../../carga/models/Departamento.md)
