---
symbol: delete_programa
kind: function
module: api/views/carga_views.py
lines: 333-335
signature_hash: sha1:3f056fbd21aabc6a2cd3c29080c9d45b0a833786
authored: true
---

# delete_programa

**Módulo:** `api/views/carga_views.py` (líneas 333-335)

## Propósito

Borrado físico (no soft-delete) de un `Programa` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_programa(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Programa](../../../carga/models/Programa.md)
