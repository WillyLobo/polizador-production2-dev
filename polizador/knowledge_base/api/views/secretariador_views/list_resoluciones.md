---
symbol: list_resoluciones
kind: function
module: api/views/secretariador_views.py
lines: 96-100
signature_hash: sha1:5379f3be87cc29fcb28377310a9f1ea4c9cd83ff
authored: true
---

# list_resoluciones

**Módulo:** `api/views/secretariador_views.py` (líneas 96-100)

## Propósito

Listado paginado (`PerPagePagination`) de `InstrumentosLegalesResoluciones`, gateado por `require_model_perm(InstrumentosLegalesResoluciones)` (permiso `view_<modelo>`). Con `?ano=` para acotar por año.

## Firma

```python
def list_resoluciones(request, ano: str=''):
```

## Uso real

`GET /v1/api/resoluciones/` — response=`List[InstrumentosLegalesResolucionesOut]`.

## Ver también

- [InstrumentosLegalesResoluciones](../../../secretariador/models/InstrumentosLegalesResoluciones.md)
