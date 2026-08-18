---
symbol: delete_vehiculo
kind: function
module: api/views/secretariador_views.py
lines: 529-531
signature_hash: sha1:d2ef4a53afb7243053bccc73294ded7e6ea2e141
authored: true
---

# delete_vehiculo

**Módulo:** `api/views/secretariador_views.py` (líneas 529-531)

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
