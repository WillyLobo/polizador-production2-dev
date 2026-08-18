---
symbol: delete_aseguradora
kind: function
module: api/views/carga_views.py
lines: 188-190
signature_hash: sha1:2fd69dd1141bee20521923e5e2fb596b3f6a239b
authored: true
---

# delete_aseguradora

**Módulo:** `api/views/carga_views.py` (líneas 188-190)

## Propósito

Borrado físico (no soft-delete) de un `Aseguradora` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_aseguradora(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Aseguradora](../../../carga/models/Aseguradora.md)
