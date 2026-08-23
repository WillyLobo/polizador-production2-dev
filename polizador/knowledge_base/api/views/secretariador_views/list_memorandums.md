---
symbol: list_memorandums
kind: function
module: api/views/secretariador_views.py
lines: 54-58
signature_hash: sha1:df5fcf5ca24ae9d31e7716b5d92aca1263db8491
authored: true
---

# list_memorandums

**Módulo:** `api/views/secretariador_views.py` (líneas 54-58)

## Propósito

Listado paginado (`PerPagePagination`) de `InstrumentosLegalesMemorandum`, gateado por `require_model_perm(InstrumentosLegalesMemorandum)` (permiso `view_<modelo>`). Con `?ano=` para acotar por año.

## Firma

```python
def list_memorandums(request, ano: str=''):
```

## Uso real

`GET /v1/api/memorandums/` — response=`List[InstrumentosLegalesMemorandumOut]`.

## Ver también

- [InstrumentosLegalesMemorandum](../../../secretariador/models/InstrumentosLegalesMemorandum.md)
