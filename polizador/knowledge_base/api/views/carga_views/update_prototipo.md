---
symbol: update_prototipo
kind: function
module: api/views/carga_views.py
lines: 1173-1178
signature_hash: sha1:b0df1202e261a6134c2c6865e3f8d2ecb594aa40
authored: true
---

# update_prototipo

**Módulo:** `api/views/carga_views.py` (líneas 1173-1178)

## Propósito

Actualización parcial de un `Prototipo` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_prototipo(request, id: int, payload: PrototipoUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`PrototipoOut`.

## Ver también

- [Prototipo](../../../carga/models/Prototipo.md)
