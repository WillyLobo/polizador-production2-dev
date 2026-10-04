---
symbol: list_rubros
kind: function
module: api/views/carga_views.py
lines: 1192-1193
signature_hash: sha1:2f82b6ead91df26555e34aea66f694b5609fa2c8
authored: true
---

# list_rubros

**Módulo:** `api/views/carga_views.py` (líneas 1192-1193)

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
