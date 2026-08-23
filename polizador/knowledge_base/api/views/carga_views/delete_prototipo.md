---
symbol: delete_prototipo
kind: function
module: api/views/carga_views.py
lines: 1182-1184
signature_hash: sha1:6e29f74459157563f0c0160d44626b65628a267c
authored: true
---

# delete_prototipo

**Módulo:** `api/views/carga_views.py` (líneas 1182-1184)

## Propósito

Borrado físico (no soft-delete) de un `Prototipo` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_prototipo(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Prototipo](../../../carga/models/Prototipo.md)
