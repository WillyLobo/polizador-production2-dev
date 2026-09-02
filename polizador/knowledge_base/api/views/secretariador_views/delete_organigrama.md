---
symbol: delete_organigrama
kind: function
module: api/views/secretariador_views.py
lines: 513-515
signature_hash: sha1:da15d8535ae83eea971c19f94485f4aef7550c25
authored: true
---
# delete_organigrama

**Módulo:** `api/views/secretariador_views.py` (líneas 513-515)

## Propósito

Borrado físico (no soft-delete) de un `Organigrama` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_organigrama(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Organigrama](../../../secretariador/models/Organigrama.md)