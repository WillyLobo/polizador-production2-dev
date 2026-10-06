---
symbol: datatable_certificados_filtro_rubro
kind: function
module: api/views/carga_views.py
lines: 1416-1422
signature_hash: sha1:9783b1d47c3ac08d487b2c28996d6c404842cb5d
authored: true
---

# datatable_certificados_filtro_rubro

**Módulo:** `api/views/carga_views.py` (líneas 1416-1422)

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
