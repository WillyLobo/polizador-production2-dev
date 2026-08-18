---
symbol: list_rubros
kind: function
module: api/views/carga_views.py
lines: 1191-1192
signature_hash: sha1:c570db7fd02fed07ed640b4abfdbc746642af252
authored: true
---

# list_rubros

**Módulo:** `api/views/carga_views.py` (líneas 1191-1192)

## Propósito

Listado paginado (`PerPagePagination`) de `CertificadoRubro`, gateado por `require_model_perm(CertificadoRubro)` (permiso `view_<modelo>`).

## Firma

```python
def list_rubros(request):
```

## Uso real

`GET /v1/api/rubros/` — response=`List[CertificadoRubroOut]`.

## Ver también

- [CertificadoRubro](../../../carga/models/CertificadoRubro.md)
