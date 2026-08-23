---
symbol: delete_localidad
kind: function
module: api/views/carga_views.py
lines: 637-639
signature_hash: sha1:7732f51c4b0aa480d3eefa2cbf4b874ee6afb4c8
authored: true
---

# delete_localidad

**Módulo:** `api/views/carga_views.py` (líneas 637-639)

## Propósito

Borrado físico (no soft-delete) de un `Localidad` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_localidad(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Localidad](../../../carga/models/Localidad.md)
