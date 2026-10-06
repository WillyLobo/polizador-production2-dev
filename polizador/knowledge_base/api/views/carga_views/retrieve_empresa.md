---
symbol: retrieve_empresa
kind: function
module: api/views/carga_views.py
lines: 235-236
signature_hash: sha1:0252829029d7bc67de960fcd8870509e4b8d07fb
authored: true
---

# retrieve_empresa

**Módulo:** `api/views/carga_views.py` (líneas 235-236)

## Propósito

Devuelve un `Empresa` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_empresa(request, id: int):
```

## Uso real

`GET /v1/api/empresa/{{id}}/` — response=`EmpresaOut`.

## Ver también

- [Empresa](../../../carga/models/Empresa.md)
