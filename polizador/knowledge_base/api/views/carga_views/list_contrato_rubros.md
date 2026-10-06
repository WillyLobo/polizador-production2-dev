---
symbol: list_contrato_rubros
kind: function
module: api/views/carga_views.py
lines: 1686-1687
signature_hash: sha1:a03e51b659bd62fac2fd2a41a48b3bae405c89ea
authored: true
---

# list_contrato_rubros

**Módulo:** `api/views/carga_views.py` (líneas 1686-1687)

## Propósito

Listado paginado (`PerPagePagination`) de `ContratoRubro`, gateado por `require_model_perm(ContratoRubro)` (permiso `view_<modelo>`). Sin endpoint `retrieve`.

## Firma

```python
def list_contrato_rubros(request):
```

## Uso real

`GET /v1/api/contrato-rubros/` — response=`List[ContratoRubroOut]`.

## Ver también

- [ContratoRubro](../../../carga/models/ContratoRubro.md)
