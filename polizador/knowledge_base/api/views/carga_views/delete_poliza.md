---
symbol: delete_poliza
kind: function
module: api/views/carga_views.py
lines: 1861-1863
signature_hash: sha1:cc04d2c9e1e9b66936e3ebdd6d707ff78b406665
authored: true
---

# delete_poliza

**Módulo:** `api/views/carga_views.py` (líneas 1861-1863)

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
