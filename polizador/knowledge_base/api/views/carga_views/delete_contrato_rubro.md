---
symbol: delete_contrato_rubro
kind: function
module: api/views/carga_views.py
lines: 1708-1710
signature_hash: sha1:6da54f7c8dc5b72b80663647f98a8101f31b66b7
authored: true
---

# delete_contrato_rubro

**Módulo:** `api/views/carga_views.py` (líneas 1708-1710)

## Propósito

Borrado físico (no soft-delete) de un `ContratoRubro` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_contrato_rubro(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [ContratoRubro](../../../carga/models/ContratoRubro.md)
