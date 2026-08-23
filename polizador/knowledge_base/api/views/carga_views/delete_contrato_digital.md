---
symbol: delete_contrato_digital
kind: function
module: api/views/carga_views.py
lines: 1718-1720
signature_hash: sha1:e9eb5f04ffabe3e4b835054dafe9c1dbd150cfd6
authored: true
---

# delete_contrato_digital

**Módulo:** `api/views/carga_views.py` (líneas 1718-1720)

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
