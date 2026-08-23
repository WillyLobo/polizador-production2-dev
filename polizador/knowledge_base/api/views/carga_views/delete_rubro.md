---
symbol: delete_rubro
kind: function
module: api/views/carga_views.py
lines: 1219-1221
signature_hash: sha1:a0ddd158516f42d36f727814f02ec19e8c66e798
authored: true
---

# delete_rubro

**Módulo:** `api/views/carga_views.py` (líneas 1219-1221)

## Propósito

Borrado físico (no soft-delete) de un `CertificadoRubro` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_rubro(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [CertificadoRubro](../../../carga/models/CertificadoRubro.md)
