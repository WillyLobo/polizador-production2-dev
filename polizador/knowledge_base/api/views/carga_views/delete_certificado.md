---
symbol: delete_certificado
kind: function
module: api/views/carga_views.py
lines: 1297-1299
signature_hash: sha1:9c931b92de9e4ddd2f0cde2b127a115cfa7a6ae7
authored: true
---

# delete_certificado

**Módulo:** `api/views/carga_views.py` (líneas 1297-1299)

## Propósito

Borrado físico (no soft-delete) de un `Certificado` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_certificado(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Certificado](../../../carga/models/Certificado.md)
