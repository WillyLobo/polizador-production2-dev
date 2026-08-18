---
symbol: delete_resolucion_directorio
kind: function
module: api/views/secretariador_views.py
lines: 157-159
signature_hash: sha1:6f12425b17259f7558a8685eee1f100621e81e60
authored: true
---

# delete_resolucion_directorio

**Módulo:** `api/views/secretariador_views.py` (líneas 157-159)

## Propósito

Borrado físico (no soft-delete) de un `InstrumentosLegalesResoluciones` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_resolucion_directorio(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [InstrumentosLegalesResoluciones](../../../secretariador/models/InstrumentosLegalesResoluciones.md)
