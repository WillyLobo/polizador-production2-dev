---
symbol: delete_poliza
kind: function
module: api/views/carga_views.py
lines: 1840-1842
signature_hash: sha1:2d8349d89aa5c10c1f6819ce0324c1c2fb12b9be
authored: true
---

# delete_poliza

**Módulo:** `api/views/carga_views.py` (líneas 1840-1842)

## Propósito

Borrado físico (no soft-delete) de un `Poliza` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_poliza(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Poliza](../../../carga/models/Poliza.md)
