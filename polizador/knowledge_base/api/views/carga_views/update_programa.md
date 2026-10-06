---
symbol: update_programa
kind: function
module: api/views/carga_views.py
lines: 324-329
signature_hash: sha1:c8e26ef7937ddfc3894a31f682476565773d368e
authored: true
---

# update_programa

**Módulo:** `api/views/carga_views.py` (líneas 324-329)

## Propósito

Actualización parcial de un `Programa` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_programa(request, id: int, payload: ProgramaUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`ProgramaOut`.

## Ver también

- [Programa](../../../carga/models/Programa.md)
