---
symbol: delete_receptor
kind: function
module: api/views/carga_views.py
lines: 115-117
signature_hash: sha1:c10e0a26c995c396a0978022abd6b4be6551df02
authored: true
---

# delete_receptor

**Módulo:** `api/views/carga_views.py` (líneas 115-117)

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
