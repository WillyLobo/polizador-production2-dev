---
symbol: update_programa
kind: function
module: api/views/carga_views.py
lines: 323-328
signature_hash: sha1:ea83547240bca6007d5a068161cae81194577e46
authored: true
---

# update_programa

**Módulo:** `api/views/carga_views.py` (líneas 323-328)

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
