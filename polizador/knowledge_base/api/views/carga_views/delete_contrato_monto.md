---
symbol: delete_contrato_monto
kind: function
module: api/views/carga_views.py
lines: 1656-1658
signature_hash: sha1:d73df502467dd759603c1c784bb03b4b4cf4167c
authored: true
---

# delete_contrato_monto

**Módulo:** `api/views/carga_views.py` (líneas 1656-1658)

## Propósito

Borrado físico (no soft-delete) de un `ContratoMonto` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_contrato_monto(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [ContratoMonto](../../../carga/models/ContratoMonto.md)
