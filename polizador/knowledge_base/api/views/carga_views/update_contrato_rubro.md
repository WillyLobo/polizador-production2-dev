---
symbol: update_contrato_rubro
kind: function
module: api/views/carga_views.py
lines: 1698-1703
signature_hash: sha1:06968e9779ea20939794ae4b8a83e6cf471c9c6b
authored: true
---

# update_contrato_rubro

**Módulo:** `api/views/carga_views.py` (líneas 1698-1703)

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
