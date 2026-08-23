---
symbol: delete_uvi
kind: function
module: api/views/carga_views.py
lines: 1758-1760
signature_hash: sha1:ef740073a53abe39b9cffa2af42cf5506f7587d5
authored: true
---

# delete_uvi

**Módulo:** `api/views/carga_views.py` (líneas 1758-1760)

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
