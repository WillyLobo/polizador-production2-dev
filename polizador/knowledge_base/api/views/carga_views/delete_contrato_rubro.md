---
symbol: delete_contrato_rubro
kind: function
module: api/views/carga_views.py
lines: 1687-1689
signature_hash: sha1:121cec32764f36f4481fde6ad6346c769352a7a4
authored: true
---

# delete_contrato_rubro

**Módulo:** `api/views/carga_views.py` (líneas 1687-1689)

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
