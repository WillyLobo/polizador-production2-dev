---
symbol: delete_certificado
kind: function
module: api/views/carga_views.py
lines: 1296-1298
signature_hash: sha1:4e9fe627930b8cf8b97aa8eb98ada2ed9decf005
authored: true
---

# delete_certificado

**Módulo:** `api/views/carga_views.py` (líneas 1296-1298)

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
