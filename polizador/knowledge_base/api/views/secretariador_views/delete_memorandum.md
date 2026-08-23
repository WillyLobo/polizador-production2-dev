---
symbol: delete_memorandum
kind: function
module: api/views/secretariador_views.py
lines: 87-89
signature_hash: sha1:be88fdd2b937e3bff9ad5d998c88c603aec9f7e8
authored: true
---

# delete_memorandum

**Módulo:** `api/views/secretariador_views.py` (líneas 87-89)

## Propósito

Borrado físico (no soft-delete) de un `InstrumentosLegalesMemorandum` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_memorandum(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [InstrumentosLegalesMemorandum](../../../secretariador/models/InstrumentosLegalesMemorandum.md)
