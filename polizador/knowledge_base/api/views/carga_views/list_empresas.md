---
symbol: list_empresas
kind: function
module: api/views/carga_views.py
lines: 221-229
signature_hash: sha1:93f4926201416ba4958fe6ffa7ffd62afb4226be
authored: true
---

# list_empresas

**Módulo:** `api/views/carga_views.py` (líneas 221-229)

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
