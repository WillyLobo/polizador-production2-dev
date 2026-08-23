---
symbol: retrieve_obra
kind: function
module: api/views/carga_views.py
lines: 764-769
signature_hash: sha1:ed5aa784ecb52613d536c07064e0c581980fe3cd
authored: true
---

# retrieve_obra

**Módulo:** `api/views/carga_views.py` (líneas 764-769)

## Propósito

Devuelve una Obra puntual, con `select_related` de empresa/región/programa/conjunto, serializada vía `_obra_out`.

## Firma

```python
def retrieve_obra(request, id: int):
```

## Uso real

`GET /v1/api/obra/{id}/` — response=`ObraOut`.

## Ver también

- [Obra](../../../carga/models/Obra.md)
- [_obra_out](_obra_out.md)
