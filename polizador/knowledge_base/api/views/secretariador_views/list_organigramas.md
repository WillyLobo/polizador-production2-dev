---
symbol: list_organigramas
kind: function
module: api/views/secretariador_views.py
lines: 494-495
signature_hash: sha1:bc0bd2151f3c0558d5328f62939cb0cf4244e452
authored: true
---

# list_organigramas

**Módulo:** `api/views/secretariador_views.py` (líneas 494-495)

## Propósito

Listado paginado (`PerPagePagination`) de `Organigrama`, gateado por `require_model_perm(Organigrama)` (permiso `view_<modelo>`). Sin `retrieve`/`update`.

## Firma

```python
def list_organigramas(request):
```

## Uso real

`GET /v1/api/organigramas/` — response=`List[OrganigramaOut]`.

## Ver también

- [Organigrama](../../../secretariador/models/Organigrama.md)
