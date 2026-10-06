---
symbol: list_prototipos
kind: function
module: api/views/carga_views.py
lines: 1152-1156
signature_hash: sha1:e72ece988ce3868e57eedf88cbe6200bb1da1c78
authored: true
---

# list_prototipos

**Módulo:** `api/views/carga_views.py` (líneas 1152-1156)

## Propósito

Listado paginado (`PerPagePagination`) de `Prototipo`, gateado por `require_model_perm(Prototipo)` (permiso `view_<modelo>`). Con `?obra=` para acotar a una Obra.

## Firma

```python
def list_prototipos(request, obra: str=''):
```

## Uso real

`GET /v1/api/prototipos/` — response=`List[PrototipoOut]`.

## Ver también

- [Prototipo](../../../carga/models/Prototipo.md)
