---
symbol: delete_uvi
kind: function
module: api/views/carga_views.py
lines: 1779-1781
signature_hash: sha1:5d60fce440c9aa1195a359fa37cb53ca1e7462ea
authored: true
---

# delete_uvi

**Módulo:** `api/views/carga_views.py` (líneas 1779-1781)

## Propósito

Borrado físico (no soft-delete) de un `Uvi` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_uvi(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Uvi](../../../carga/models/Uvi.md)
