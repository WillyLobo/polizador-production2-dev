---
symbol: list_aseguradoras
kind: function
module: api/views/carga_views.py
lines: 161-162
signature_hash: sha1:ee19b24f9bbcbf0ee26ab6106a91ccbaae111ff2
authored: true
---

# list_aseguradoras

**Módulo:** `api/views/carga_views.py` (líneas 161-162)

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
