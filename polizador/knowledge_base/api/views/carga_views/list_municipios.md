---
symbol: list_municipios
kind: function
module: api/views/carga_views.py
lines: 523-527
signature_hash: sha1:0127f65b20acf401217ff7885fabf6a4f35cad16
authored: true
---

# list_municipios

**Módulo:** `api/views/carga_views.py` (líneas 523-527)

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
