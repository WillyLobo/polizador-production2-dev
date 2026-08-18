---
symbol: retrieve_empresa
kind: function
module: api/views/carga_views.py
lines: 234-235
signature_hash: sha1:74d20ae1976dcba4a4be1a56d1eb94fe52369f76
authored: true
---

# retrieve_empresa

**Módulo:** `api/views/carga_views.py` (líneas 234-235)

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
