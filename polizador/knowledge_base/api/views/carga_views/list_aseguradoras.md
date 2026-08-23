---
symbol: list_aseguradoras
kind: function
module: api/views/carga_views.py
lines: 160-161
signature_hash: sha1:0f6064b0fa8245fdfd545f216583a650dc3e8d26
authored: true
---

# list_aseguradoras

**Módulo:** `api/views/carga_views.py` (líneas 160-161)

## Propósito

Listado paginado (`PerPagePagination`) de `Aseguradora`, gateado por `require_model_perm(Aseguradora)` (permiso `view_<modelo>`).

## Firma

```python
def list_aseguradoras(request):
```

## Uso real

`GET /v1/api/aseguradoras/` — response=`List[AseguradoraOut]`.

## Ver también

- [Aseguradora](../../../carga/models/Aseguradora.md)
