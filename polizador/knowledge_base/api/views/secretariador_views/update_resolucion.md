---
symbol: update_resolucion
kind: function
module: api/views/secretariador_views.py
lines: 119-124
signature_hash: sha1:62c5bc78efea1c705088c8bb88e8d7ed0e776e52
authored: true
---

# update_resolucion

**Módulo:** `api/views/secretariador_views.py` (líneas 119-124)

## Propósito

Actualización parcial de un `InstrumentosLegalesResoluciones` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_resolucion(request, id: int, payload: ResolucionUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`InstrumentosLegalesResolucionesOut`.

## Ver también

- [InstrumentosLegalesResoluciones](../../../secretariador/models/InstrumentosLegalesResoluciones.md)
