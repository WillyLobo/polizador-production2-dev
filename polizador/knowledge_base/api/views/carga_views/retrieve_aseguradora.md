---
symbol: retrieve_aseguradora
kind: function
module: api/views/carga_views.py
lines: 167-168
signature_hash: sha1:a0b7c5d412dabd319cd2cf8f2ebabf18ffc1804f
authored: true
---

# retrieve_aseguradora

**Módulo:** `api/views/carga_views.py` (líneas 167-168)

## Propósito

Devuelve un `Aseguradora` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_aseguradora(request, id: int):
```

## Uso real

`GET /v1/api/aseguradora/{{id}}/` — response=`AseguradoraOut`.

## Ver también

- [Aseguradora](../../../carga/models/Aseguradora.md)
