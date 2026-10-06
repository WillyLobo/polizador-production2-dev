---
symbol: delete_departamento_carga
kind: function
module: api/views/carga_views.py
lines: 492-494
signature_hash: sha1:49c491468cf3af343456c90a47bf2485e2d1f33c
authored: true
---

# delete_departamento_carga

**Módulo:** `api/views/carga_views.py` (líneas 492-494)

## Propósito

Borrado físico (no soft-delete) de un `Departamento` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_departamento_carga(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Departamento](../../../carga/models/Departamento.md)
