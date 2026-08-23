---
symbol: delete_direccion
kind: function
module: api/views/personalizador_views.py
lines: 89-91
signature_hash: sha1:d1fe07ca573f98fd97512500f7e64de5736241af
authored: true
---

# delete_direccion

**Módulo:** `api/views/personalizador_views.py` (líneas 89-91)

## Propósito

Borrado físico (no soft-delete) de un `Direccion` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_direccion(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Direccion](../../../personalizador/models/Direccion.md)
