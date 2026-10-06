---
symbol: retrieve_contrato
kind: function
module: api/views/carga_views.py
lines: 1601-1602
signature_hash: sha1:468ec4b0143aa10053aede0bab5e39f22f43009f
authored: true
---

# retrieve_contrato

**Módulo:** `api/views/carga_views.py` (líneas 1601-1602)

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
