---
symbol: delete_resolucion
kind: function
module: api/views/secretariador_views.py
lines: 129-131
signature_hash: sha1:045fcf9755c9cc62065faadd003970db370b24a3
authored: true
---

# delete_resolucion

**Módulo:** `api/views/secretariador_views.py` (líneas 129-131)

## Propósito

Borrado físico (no soft-delete) de un `InstrumentosLegalesResoluciones` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_resolucion(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [InstrumentosLegalesResoluciones](../../../secretariador/models/InstrumentosLegalesResoluciones.md)
