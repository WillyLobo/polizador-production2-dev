---
symbol: list_resoluciones_directorio
kind: function
module: api/views/secretariador_views.py
lines: 138-142
signature_hash: sha1:80319c5cf42db3b61194bac112bd4e606390204a
authored: true
---

# list_resoluciones_directorio

**Módulo:** `api/views/secretariador_views.py` (líneas 138-142)

## Propósito

Listado paginado (`PerPagePagination`) de `InstrumentosLegalesResoluciones`, gateado por `require_model_perm(InstrumentosLegalesResoluciones)` (permiso `view_<modelo>`). Variante acotada a `instrumentolegalresoluciones_tipo='D'` (Directorio) del mismo modelo que `list_resoluciones` — no un modelo distinto.

## Firma

```python
def list_resoluciones_directorio(request, ano: str=''):
```

## Uso real

`GET /v1/api/resoluciones-directorio/` — response=`List[InstrumentosLegalesResolucionesOut]`.

## Ver también

- [InstrumentosLegalesResoluciones](../../../secretariador/models/InstrumentosLegalesResoluciones.md)
