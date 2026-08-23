---
symbol: retrieve_comisionado
kind: function
module: api/views/secretariador_views.py
lines: 473-474
signature_hash: sha1:e856de0e6068ce829488c0c8a8f0d4d01310a669
authored: true
---

# retrieve_comisionado

**Módulo:** `api/views/secretariador_views.py` (líneas 473-474)

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
