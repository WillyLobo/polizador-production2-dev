---
symbol: update_empresa
kind: function
module: api/views/carga_views.py
lines: 246-251
signature_hash: sha1:6b8ce7d6c373eac470e2beae4c2961ecec077123
authored: true
---

# update_empresa

**Módulo:** `api/views/carga_views.py` (líneas 246-251)

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
