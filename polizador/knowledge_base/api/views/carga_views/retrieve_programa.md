---
symbol: retrieve_programa
kind: function
module: api/views/carga_views.py
lines: 312-313
signature_hash: sha1:6438d5aef486111aea38965a10f5e951722a6518
authored: true
---

# retrieve_programa

**Módulo:** `api/views/carga_views.py` (líneas 312-313)

## Propósito

Devuelve un `Programa` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_programa(request, id: int):
```

## Uso real

`GET /v1/api/programa/{{id}}/` — response=`ProgramaOut`.

## Ver también

- [Programa](../../../carga/models/Programa.md)
