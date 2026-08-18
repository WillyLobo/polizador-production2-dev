---
symbol: update_aseguradora
kind: function
module: api/views/carga_views.py
lines: 178-183
signature_hash: sha1:d2fd2355701da27330b1545cb5b6b13c0a71a5aa
authored: true
---

# update_aseguradora

**Módulo:** `api/views/carga_views.py` (líneas 178-183)

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
