---
symbol: retrieve_aseguradora
kind: function
module: api/views/carga_views.py
lines: 166-167
signature_hash: sha1:9a3a0b0778107ed7cbfe20656ac3e10895cee334
authored: true
---

# retrieve_aseguradora

**Módulo:** `api/views/carga_views.py` (líneas 166-167)

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
