---
symbol: list_contrato_rubros
kind: function
module: api/views/carga_views.py
lines: 1665-1666
signature_hash: sha1:c99f08fe7e9622a5b0f9b06f0d2239c8656b8cae
authored: true
---

# list_contrato_rubros

**Módulo:** `api/views/carga_views.py` (líneas 1665-1666)

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
