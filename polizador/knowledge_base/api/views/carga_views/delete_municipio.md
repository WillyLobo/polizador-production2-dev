---
symbol: delete_municipio
kind: function
module: api/views/carga_views.py
lines: 554-556
signature_hash: sha1:760877da01dc5236337fbeaab152b072397cda96
authored: true
---

# delete_municipio

**Módulo:** `api/views/carga_views.py` (líneas 554-556)

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
