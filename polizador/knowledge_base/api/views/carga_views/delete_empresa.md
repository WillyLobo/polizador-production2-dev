---
symbol: delete_empresa
kind: function
module: api/views/carga_views.py
lines: 257-259
signature_hash: sha1:3583254c2d366954bf1db906e86f57776aa34fb9
authored: true
---

# delete_empresa

**Módulo:** `api/views/carga_views.py` (líneas 257-259)

## Propósito

Borrado físico (no soft-delete) de un `Empresa` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_empresa(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Empresa](../../../carga/models/Empresa.md)
