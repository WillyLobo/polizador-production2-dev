---
symbol: delete_localidad
kind: function
module: api/views/carga_views.py
lines: 638-640
signature_hash: sha1:c965f6c66da34307b035d68d6b689dc193f1923c
authored: true
---

# delete_localidad

**Módulo:** `api/views/carga_views.py` (líneas 638-640)

## Propósito

Borrado físico (no soft-delete) de un `Localidad` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_localidad(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Localidad](../../../carga/models/Localidad.md)
