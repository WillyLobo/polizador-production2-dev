---
symbol: datatable_certificados_filtro_rubro
kind: function
module: api/views/carga_views.py
lines: 1415-1421
signature_hash: sha1:0edd48acbcc8fd8b2413428e535f6f45fdb93583
authored: true
---

# datatable_certificados_filtro_rubro

**Módulo:** `api/views/carga_views.py` (líneas 1415-1421)

## Propósito

Choices `(id, nombre)` de CertificadoRubro efectivamente usados por algún Certificado.

## Firma

```python
def datatable_certificados_filtro_rubro(request):
```

## Uso real

`GET /v1/api/datatables/certificados/filtro-rubro/`.

## Ver también

- [CertificadoRubro](../../../carga/models/CertificadoRubro.md)
