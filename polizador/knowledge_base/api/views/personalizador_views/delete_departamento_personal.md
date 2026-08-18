---
symbol: delete_departamento_personal
kind: function
module: api/views/personalizador_views.py
lines: 110-112
signature_hash: sha1:84f5f5424ddfb9c1193b15ff6a0fa58d401736b0
authored: true
---

# delete_departamento_personal

**Módulo:** `api/views/personalizador_views.py` (líneas 110-112)

## Propósito

Borrado físico (no soft-delete) de un `Departamento` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_departamento_personal(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Departamento](../../../personalizador/models/Departamento.md)
