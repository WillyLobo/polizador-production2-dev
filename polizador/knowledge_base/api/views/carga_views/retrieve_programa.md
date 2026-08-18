---
symbol: retrieve_programa
kind: function
module: api/views/carga_views.py
lines: 311-312
signature_hash: sha1:0a6b087aa12c4210db6bd8dc02462371e7fa71fb
authored: true
---

# retrieve_programa

**Módulo:** `api/views/carga_views.py` (líneas 311-312)

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
