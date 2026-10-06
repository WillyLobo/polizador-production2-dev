---
symbol: list_empresas
kind: function
module: api/views/carga_views.py
lines: 222-230
signature_hash: sha1:7bd31e2dc64289798cfe3406509e9452f6a48902
authored: true
---

# list_empresas

**Módulo:** `api/views/carga_views.py` (líneas 222-230)

## Propósito

Listado paginado (`PerPagePagination`) de `Empresa`, gateado por `require_model_perm(Empresa)` (permiso `view_<modelo>`). Con `?q=` de texto libre: filtra por nombre, CUIT o titular (`Q` OR).

## Firma

```python
def list_empresas(request, q: str=''):
```

## Uso real

`GET /v1/api/empresas/` — response=`List[EmpresaOut]`.

## Ver también

- [Empresa](../../../carga/models/Empresa.md)
