---
symbol: update_empresa
kind: function
module: api/views/carga_views.py
lines: 247-252
signature_hash: sha1:e3bf7f0851e1e7185184eeccdb11a02042bbf9a6
authored: true
---

# update_empresa

**Módulo:** `api/views/carga_views.py` (líneas 247-252)

## Propósito

Actualización parcial de un `Empresa` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_empresa(request, id: int, payload: EmpresaUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`EmpresaOut`.

## Ver también

- [Empresa](../../../carga/models/Empresa.md)
