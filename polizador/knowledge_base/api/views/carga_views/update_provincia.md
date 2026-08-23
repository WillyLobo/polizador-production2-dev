---
symbol: update_provincia
kind: function
module: api/views/carga_views.py
lines: 383-388
signature_hash: sha1:3d10b02964b3f1aa5e96ef506101bd7a3d8b1598
authored: true
---

# update_provincia

**Módulo:** `api/views/carga_views.py` (líneas 383-388)

## Propósito

Actualización parcial de un `Provincia` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_provincia(request, id: int, payload: ProvinciaUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`ProvinciaOut`.

## Ver también

- [Provincia](../../../carga/models/Provincia.md)
