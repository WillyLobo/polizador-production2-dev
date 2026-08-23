---
symbol: delete_indec
kind: function
module: api/views/carga_views.py
lines: 1798-1800
signature_hash: sha1:678eff12574dc646c982404925edf2f04dc70d32
authored: true
---

# delete_indec

**Módulo:** `api/views/carga_views.py` (líneas 1798-1800)

## Propósito

Borrado físico (no soft-delete) de un `INDEC` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_indec(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [INDEC](../../../carga/models/INDEC.md)
