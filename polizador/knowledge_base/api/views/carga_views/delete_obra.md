---
symbol: delete_obra
kind: function
module: api/views/carga_views.py
lines: 813-815
signature_hash: sha1:0ab9fbe962b41b38a0013908eabae8b80120a4b3
authored: true
---

# delete_obra

**Módulo:** `api/views/carga_views.py` (líneas 813-815)

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
