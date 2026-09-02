---
symbol: delete_incorporacion
kind: function
module: api/views/secretariador_views.py
lines: 842-844
signature_hash: sha1:f6d8293d4d484ea0dff1c224dc289caafbdc0334
authored: true
---
# delete_incorporacion

**Módulo:** `api/views/secretariador_views.py` (líneas 842-844)

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