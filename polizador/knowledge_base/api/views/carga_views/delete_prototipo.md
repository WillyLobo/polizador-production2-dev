---
symbol: delete_prototipo
kind: function
module: api/views/carga_views.py
lines: 1183-1185
signature_hash: sha1:51c599a818e0e6170b676464512482df48f094b9
authored: true
---

# delete_prototipo

**Módulo:** `api/views/carga_views.py` (líneas 1183-1185)

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
