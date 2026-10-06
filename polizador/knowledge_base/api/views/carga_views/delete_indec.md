---
symbol: delete_indec
kind: function
module: api/views/carga_views.py
lines: 1819-1821
signature_hash: sha1:df624de67235d9f9a79cb68c2878dc056acf9ec4
authored: true
---

# delete_indec

**Módulo:** `api/views/carga_views.py` (líneas 1819-1821)

## Propósito

Borrado físico (no soft-delete) de un `INDEC` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_indec(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [INDEC](../../../carga/models/INDEC.md)
