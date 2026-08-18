---
symbol: delete_empresa
kind: function
module: api/views/carga_views.py
lines: 256-258
signature_hash: sha1:9a44496c820dd9d6dc4e2f155476cb3412877cb4
authored: true
---

# delete_empresa

**Módulo:** `api/views/carga_views.py` (líneas 256-258)

## Propósito

Borrado físico (no soft-delete) de un `Empresa` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_empresa(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Empresa](../../../carga/models/Empresa.md)
