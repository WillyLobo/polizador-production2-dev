---
symbol: delete_decreto
kind: function
module: api/views/secretariador_views.py
lines: 189-191
signature_hash: sha1:f641f3ebefdc2cc118f7c8215476e830c99f295f
authored: true
---

# delete_decreto

**Módulo:** `api/views/secretariador_views.py` (líneas 189-191)

## Propósito

Borrado físico (no soft-delete) de un `InstrumentosLegalesDecretos` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_decreto(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [InstrumentosLegalesDecretos](../../../secretariador/models/InstrumentosLegalesDecretos.md)
