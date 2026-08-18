---
symbol: update_localidad
kind: function
module: api/views/carga_views.py
lines: 627-632
signature_hash: sha1:90d217742e260deb3c34da11bbed26f6e5fed332
authored: true
---

# update_localidad

**Módulo:** `api/views/carga_views.py` (líneas 627-632)

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
