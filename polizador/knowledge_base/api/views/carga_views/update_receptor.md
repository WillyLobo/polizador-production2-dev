---
symbol: update_receptor
kind: function
module: api/views/carga_views.py
lines: 104-109
signature_hash: sha1:b616c9fda214c8c74bff3455120d8a7abcc8a360
authored: true
---

# update_receptor

**Módulo:** `api/views/carga_views.py` (líneas 104-109)

## Propósito

Actualización parcial de un `Receptor` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_receptor(request, id: int, payload: ReceptorUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`ReceptorOut`.

## Ver también

- [Receptor](../../../carga/models/Receptor.md)
