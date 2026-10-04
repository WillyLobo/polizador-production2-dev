---
symbol: list_localidades
kind: function
module: api/views/carga_views.py
lines: 607-611
signature_hash: sha1:9bdbccadaa8745b49f14f8d228903380dd296a3b
authored: true
---

# list_localidades

**Módulo:** `api/views/carga_views.py` (líneas 607-611)

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
