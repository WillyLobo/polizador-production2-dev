---
symbol: delete_contrato_digital
kind: function
module: api/views/carga_views.py
lines: 1739-1741
signature_hash: sha1:5c8ad3dc16d93df97cd9f0cdcf9e1aa613aa5095
authored: true
---

# delete_contrato_digital

**Módulo:** `api/views/carga_views.py` (líneas 1739-1741)

## Propósito

Borrado físico (no soft-delete) de un `ContratosDigitales` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_contrato_digital(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [ContratosDigitales](../../../carga/models/ContratosDigitales.md)
