---
symbol: delete_municipio
kind: function
module: api/views/carga_views.py
lines: 555-557
signature_hash: sha1:19b8775ad4b87d0052b1eb426b5233e1db655d4e
authored: true
---

# delete_municipio

**Módulo:** `api/views/carga_views.py` (líneas 555-557)

## Propósito

Borrado físico (no soft-delete) de un `Municipio` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_municipio(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Municipio](../../../carga/models/Municipio.md)
