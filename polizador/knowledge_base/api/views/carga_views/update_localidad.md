---
symbol: update_localidad
kind: function
module: api/views/carga_views.py
lines: 628-633
signature_hash: sha1:dbfabca5178f7c3aaefa62771920d8ac16e2f99a
authored: true
---

# update_localidad

**Módulo:** `api/views/carga_views.py` (líneas 628-633)

## Propósito

Actualización parcial de un `Localidad` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_localidad(request, id: int, payload: LocalidadUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`LocalidadOut`.

## Ver también

- [Localidad](../../../carga/models/Localidad.md)
