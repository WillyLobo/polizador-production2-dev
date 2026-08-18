---
symbol: update_contrato
kind: function
module: api/views/carga_views.py
lines: 1612-1617
signature_hash: sha1:749d9aad008078137baddee6913360f9097aa555
authored: true
---

# update_contrato

**Módulo:** `api/views/carga_views.py` (líneas 1612-1617)

## Propósito

Actualización parcial de un `Contrato` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_contrato(request, id: int, payload: ContratoUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`ContratoOut`.

## Ver también

- [Contrato](../../../carga/models/Contrato.md)
