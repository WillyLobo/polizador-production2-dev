---
symbol: list_direcciones
kind: function
module: api/views/personalizador_views.py
lines: 77-78
signature_hash: sha1:60d3a4e84189cc5c21c952030ea4281244ac29a2
authored: true
---

# list_direcciones

**Módulo:** `api/views/personalizador_views.py` (líneas 77-78)

## Propósito

Listado paginado (`PerPagePagination`) de `Direccion`, gateado por `require_model_perm(Direccion)` (permiso `view_<modelo>`). Mismo patrón que Gerencia: sin `retrieve`/`update`.

## Firma

```python
def list_direcciones(request):
```

## Uso real

`GET /v1/api/direcciones/` — response=`List[DireccionOut]`.

## Ver también

- [Direccion](../../../personalizador/models/Direccion.md)
