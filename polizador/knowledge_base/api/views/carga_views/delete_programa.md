---
symbol: delete_programa
kind: function
module: api/views/carga_views.py
lines: 334-336
signature_hash: sha1:8822d1555aceae4a7d94f460a489cf4fc3760bec
authored: true
---

# delete_programa

**Módulo:** `api/views/carga_views.py` (líneas 334-336)

## Propósito

Borrado físico (no soft-delete) de un `Programa` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_programa(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Programa](../../../carga/models/Programa.md)
