---
symbol: list_decretos
kind: function
module: api/views/secretariador_views.py
lines: 166-170
signature_hash: sha1:a9c89f894f3b24e242c57d7503a74bb421b5c915
authored: true
---

# list_decretos

**Módulo:** `api/views/secretariador_views.py` (líneas 166-170)

## Propósito

Listado paginado (`PerPagePagination`) de `InstrumentosLegalesDecretos`, gateado por `require_model_perm(InstrumentosLegalesDecretos)` (permiso `view_<modelo>`). Con `?ano=` para acotar por año. Sin `update` — un Decreto no se edita desde esta API.

## Firma

```python
def list_decretos(request, ano: str=''):
```

## Uso real

`GET /v1/api/decretos/` — response=`List[InstrumentosLegalesDecretosOut]`.

## Ver también

- [InstrumentosLegalesDecretos](../../../secretariador/models/InstrumentosLegalesDecretos.md)
