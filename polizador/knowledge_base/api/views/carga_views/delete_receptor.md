---
symbol: delete_receptor
kind: function
module: api/views/carga_views.py
lines: 114-116
signature_hash: sha1:2b50a675aec9eccb0abb9cdd89949f40eaefa268
authored: true
---

# delete_receptor

**Módulo:** `api/views/carga_views.py` (líneas 114-116)

## Propósito

Borrado físico (no soft-delete) de un `Receptor` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_receptor(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Receptor](../../../carga/models/Receptor.md)
