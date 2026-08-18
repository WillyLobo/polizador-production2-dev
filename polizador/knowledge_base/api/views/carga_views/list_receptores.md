---
symbol: list_receptores
kind: function
module: api/views/carga_views.py
lines: 86-87
signature_hash: sha1:15baf9f17a304f2c64ac9499ee520862a6534db4
authored: true
---

# list_receptores

**Módulo:** `api/views/carga_views.py` (líneas 86-87)

## Propósito

Listado paginado (`PerPagePagination`) de `Receptor`, gateado por `require_model_perm(Receptor)` (permiso `view_<modelo>`).

## Firma

```python
def list_receptores(request):
```

## Uso real

`GET /v1/api/receptores/` — response=`List[ReceptorOut]`.

## Ver también

- [Receptor](../../../carga/models/Receptor.md)
