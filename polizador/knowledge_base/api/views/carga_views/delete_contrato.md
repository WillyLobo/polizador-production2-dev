---
symbol: delete_contrato
kind: function
module: api/views/carga_views.py
lines: 1622-1624
signature_hash: sha1:b9c72c9d7fd539c0712be8bfb25058053f94e2b3
authored: true
---

# delete_contrato

**Módulo:** `api/views/carga_views.py` (líneas 1622-1624)

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
