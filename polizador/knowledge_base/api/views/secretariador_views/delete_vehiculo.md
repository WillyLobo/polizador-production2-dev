---
symbol: delete_vehiculo
kind: function
module: api/views/secretariador_views.py
lines: 536-538
signature_hash: sha1:b8cd7151c0bea1a58233366c3f32780ecf9636ef
authored: true
---
# delete_vehiculo

**Módulo:** `api/views/secretariador_views.py` (líneas 536-538)

## Propósito

Borrado físico (no soft-delete) de un `Vehiculo` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_vehiculo(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [Vehiculo](../../../secretariador/models/Vehiculo.md)