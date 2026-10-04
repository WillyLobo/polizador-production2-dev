---
symbol: delete_provincia
kind: function
module: api/views/carga_views.py
lines: 394-396
signature_hash: sha1:385f8e8ddd660d90f8b9980c59bd32f3415a85c6
authored: true
---

# delete_provincia

**Módulo:** `api/views/carga_views.py` (líneas 394-396)

## Propósito

Borrado físico (no soft-delete) de un `Provincia` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_provincia(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Provincia](../../../carga/models/Provincia.md)
