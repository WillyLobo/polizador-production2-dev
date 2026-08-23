---
symbol: update_departamento_carga
kind: function
module: api/views/carga_views.py
lines: 481-486
signature_hash: sha1:2877373060f43b6544530639e4ad18ed6291ed83
authored: true
---

# update_departamento_carga

**Módulo:** `api/views/carga_views.py` (líneas 481-486)

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
