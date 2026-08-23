---
symbol: list_localidades
kind: function
module: api/views/carga_views.py
lines: 606-610
signature_hash: sha1:c3d9cd7ca89543e0582ba4c3999aff8f4295ce4d
authored: true
---

# list_localidades

**Módulo:** `api/views/carga_views.py` (líneas 606-610)

## Propósito

Listado paginado (`PerPagePagination`) de `Localidad`, gateado por `require_model_perm(Localidad)` (permiso `view_<modelo>`). Con `?departamento=` para acotar al Departamento elegido.

## Firma

```python
def list_localidades(request, departamento: str=''):
```

## Uso real

`GET /v1/api/localidades/` — response=`List[LocalidadOut]`.

## Ver también

- [Localidad](../../../carga/models/Localidad.md)
