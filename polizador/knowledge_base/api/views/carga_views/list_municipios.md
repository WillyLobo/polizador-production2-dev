---
symbol: list_municipios
kind: function
module: api/views/carga_views.py
lines: 524-528
signature_hash: sha1:21b3f5435c84ed6a7eac67037825895b367f7c82
authored: true
---

# list_municipios

**Módulo:** `api/views/carga_views.py` (líneas 524-528)

## Propósito

Listado paginado (`PerPagePagination`) de `Municipio`, gateado por `require_model_perm(Municipio)` (permiso `view_<modelo>`). Con `?departamento=` para acotar al Departamento elegido.

## Firma

```python
def list_municipios(request, departamento: str=''):
```

## Uso real

`GET /v1/api/municipios/` — response=`List[MunicipioOut]`.

## Ver también

- [Municipio](../../../carga/models/Municipio.md)
