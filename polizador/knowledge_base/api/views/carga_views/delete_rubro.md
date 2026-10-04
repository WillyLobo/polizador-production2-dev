---
symbol: delete_rubro
kind: function
module: api/views/carga_views.py
lines: 1220-1222
signature_hash: sha1:1d74012ac0c78cc2c280e7642b923f8d4b61c33d
authored: true
---

# delete_rubro

**Módulo:** `api/views/carga_views.py` (líneas 1220-1222)

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
