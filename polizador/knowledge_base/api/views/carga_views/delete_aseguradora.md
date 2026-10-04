---
symbol: delete_aseguradora
kind: function
module: api/views/carga_views.py
lines: 189-191
signature_hash: sha1:9670347dc06a193d780968e5c58b01df4097f4f2
authored: true
---

# delete_aseguradora

**Módulo:** `api/views/carga_views.py` (líneas 189-191)

## Propósito

Borrado físico (no soft-delete) de un `Aseguradora` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_aseguradora(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Aseguradora](../../../carga/models/Aseguradora.md)
