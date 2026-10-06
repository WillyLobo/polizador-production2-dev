---
symbol: update_obra
kind: function
module: api/views/carga_views.py
lines: 794-809
signature_hash: sha1:3ce74431ea9d1025f1375367d4df247899f80c18
authored: true
---

# update_obra

**Módulo:** `api/views/carga_views.py` (líneas 794-809)

## Propósito

Mismo tratamiento de M2M que `create_obra`, pero solo para las claves presentes en el payload (`exclude_unset=True`) — no toca un M2M que el cliente no envió.

## Firma

```python
def update_obra(request, id: int, payload: ObraUpdate):
```

## Uso real

`PUT /v1/api/obra/{id}/` — response=`ObraOut`.

## Ver también

- [Obra](../../../carga/models/Obra.md)
- [create_obra](create_obra.md)
