---
symbol: delete_organigrama
kind: function
module: api/views/secretariador_views.py
lines: 506-508
signature_hash: sha1:172ad72d1e7e99eeb23185b18e44f3b4d078f917
authored: true
---

# delete_organigrama

**Módulo:** `api/views/secretariador_views.py` (líneas 506-508)

## Propósito

Borrado físico (no soft-delete) de un `Organigrama` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_organigrama(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Organigrama](../../../secretariador/models/Organigrama.md)
