---
symbol: update_contrato_rubro
kind: function
module: api/views/carga_views.py
lines: 1677-1682
signature_hash: sha1:6276e640b7db932cee504ace337cf6a1b3979da0
authored: true
---

# update_contrato_rubro

**Módulo:** `api/views/carga_views.py` (líneas 1677-1682)

## Propósito

Actualización parcial de un `ContratoRubro` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_contrato_rubro(request, id: int, payload: ContratoRubroUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`ContratoRubroOut`.

## Ver también

- [ContratoRubro](../../../carga/models/ContratoRubro.md)
