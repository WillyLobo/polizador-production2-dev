---
symbol: retrieve_contrato
kind: function
module: api/views/carga_views.py
lines: 1600-1601
signature_hash: sha1:e5b90d9b1d7afa968f3379704dc3763f0f4eb533
authored: true
---

# retrieve_contrato

**Módulo:** `api/views/carga_views.py` (líneas 1600-1601)

## Propósito

Devuelve un `Contrato` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_contrato(request, id: int):
```

## Uso real

`GET /v1/api/contrato/{{id}}/` — response=`ContratoOut`.

## Ver también

- [Contrato](../../../carga/models/Contrato.md)
