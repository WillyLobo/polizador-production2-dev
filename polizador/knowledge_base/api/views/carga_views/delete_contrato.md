---
symbol: delete_contrato
kind: function
module: api/views/carga_views.py
lines: 1623-1625
signature_hash: sha1:c0a545af02620ca0108d5ddfbc3d1a8df75340a1
authored: true
---

# delete_contrato

**Módulo:** `api/views/carga_views.py` (líneas 1623-1625)

## Propósito

Borrado físico (no soft-delete) de un `Contrato` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_contrato(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Contrato](../../../carga/models/Contrato.md)
