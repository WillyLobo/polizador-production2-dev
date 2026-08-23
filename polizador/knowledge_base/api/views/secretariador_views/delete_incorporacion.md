---
symbol: delete_incorporacion
kind: function
module: api/views/secretariador_views.py
lines: 835-837
signature_hash: sha1:e28dac94ec482570b725c02d1dbefa85fd270cc7
authored: true
---

# delete_incorporacion

**Módulo:** `api/views/secretariador_views.py` (líneas 835-837)

## Propósito

Borrado físico (no soft-delete) de un `Incorporacion` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_incorporacion(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Incorporacion](../../../secretariador/models/Incorporacion.md)
