---
symbol: list_departamentos_carga
kind: function
module: api/views/carga_views.py
lines: 464-465
signature_hash: sha1:7bc27d7b4e5a11f0de01b690ef063e1dd8a77460
authored: true
---

# list_departamentos_carga

**Módulo:** `api/views/carga_views.py` (líneas 464-465)

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
