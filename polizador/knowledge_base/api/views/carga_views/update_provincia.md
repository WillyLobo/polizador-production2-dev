---
symbol: update_provincia
kind: function
module: api/views/carga_views.py
lines: 384-389
signature_hash: sha1:957c39349c3c02f0aac53be35875d7d7b0d31d57
authored: true
---

# update_provincia

**Módulo:** `api/views/carga_views.py` (líneas 384-389)

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
