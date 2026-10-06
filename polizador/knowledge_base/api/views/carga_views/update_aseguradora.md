---
symbol: update_aseguradora
kind: function
module: api/views/carga_views.py
lines: 179-184
signature_hash: sha1:49e3ab7efa2cac83725fe68b52bd6149fd493ef6
authored: true
---

# update_aseguradora

**Módulo:** `api/views/carga_views.py` (líneas 179-184)

## Propósito

Actualización parcial de un `Aseguradora` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_aseguradora(request, id: int, payload: AseguradoraUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`AseguradoraOut`.

## Ver también

- [Aseguradora](../../../carga/models/Aseguradora.md)
