---
symbol: delete_contrato_monto
kind: function
module: api/views/carga_views.py
lines: 1677-1679
signature_hash: sha1:70c5ab20fe4438b3f1c959705b05604dc25766cc
authored: true
---

# delete_contrato_monto

**Módulo:** `api/views/carga_views.py` (líneas 1677-1679)

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
