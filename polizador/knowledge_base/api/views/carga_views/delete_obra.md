---
symbol: delete_obra
kind: function
module: api/views/carga_views.py
lines: 814-816
signature_hash: sha1:8a8d2105b5f2af3a7c8cd5f5187ab49ad54c13f3
authored: true
---

# delete_obra

**Módulo:** `api/views/carga_views.py` (líneas 814-816)

## Propósito

Borrado físico de una Obra por `id`.

## Firma

```python
def delete_obra(request, id: int):
```

## Uso real

`DELETE /v1/api/obra/{id}/`.

## Ver también

- [Obra](../../../carga/models/Obra.md)
