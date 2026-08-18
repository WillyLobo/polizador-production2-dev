---
symbol: update_prototipo
kind: function
module: api/views/carga_views.py
lines: 1172-1177
signature_hash: sha1:59e67320d73a3d586ff5319e3abdcff03eaa609a
authored: true
---

# update_prototipo

**Módulo:** `api/views/carga_views.py` (líneas 1172-1177)

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
