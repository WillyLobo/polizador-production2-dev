---
symbol: retrieve_comisionado
kind: function
module: api/views/secretariador_views.py
lines: 480-481
signature_hash: sha1:dce764bf02bb5b4bdc9a98cafc80fec4043714da
authored: true
---
# retrieve_comisionado

**Módulo:** `api/views/secretariador_views.py` (líneas 480-481)

## Propósito

Devuelve un `Agente` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_comisionado(request, id: int):
```

## Uso real

`GET /v1/api/comisionado/{{id}}/` — response=`AgenteOut`.

## Ver también

- [Agente](../../../secretariador/models/Agente.md)