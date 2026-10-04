---
symbol: update_departamento_carga
kind: function
module: api/views/carga_views.py
lines: 482-487
signature_hash: sha1:d3458a1fe21404e16373cd2b7ca54da0fc20ff92
authored: true
---

# update_departamento_carga

**Módulo:** `api/views/carga_views.py` (líneas 482-487)

## Propósito

Actualización parcial de un `Departamento` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_departamento_carga(request, id: int, payload: DepartamentoCargaUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`DepartamentoOut`.

## Ver también

- [Departamento](../../../carga/models/Departamento.md)
