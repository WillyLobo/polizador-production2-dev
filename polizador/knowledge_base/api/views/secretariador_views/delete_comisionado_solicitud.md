---
symbol: delete_comisionado_solicitud
kind: function
module: api/views/secretariador_views.py
lines: 811-813
signature_hash: sha1:ef2017d748ce3910f90ef4a05144147c1daf2ad5
authored: true
---

# delete_comisionado_solicitud

**Módulo:** `api/views/secretariador_views.py` (líneas 811-813)

## Propósito

Borrado físico (no soft-delete) de un `ComisionadoSolicitud` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_comisionado_solicitud(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [ComisionadoSolicitud](../../../secretariador/models/ComisionadoSolicitud.md)
