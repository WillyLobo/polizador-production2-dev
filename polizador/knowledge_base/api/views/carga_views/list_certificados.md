---
symbol: list_certificados
kind: function
module: api/views/carga_views.py
lines: 1265-1269
signature_hash: sha1:bc9d3e88b80a5031836e6809ea96051cc501ddfc
authored: true
---

# list_certificados

**Módulo:** `api/views/carga_views.py` (líneas 1265-1269)

## Propósito

Listado paginado (`PerPagePagination`) de `Certificado`, gateado por `require_model_perm(Certificado)` (permiso `view_<modelo>`). Con `?obra=` para acotar a una Obra. Requiere además el grupo `gciaoperativa_usuarios` (`get_group_perms`), no solo el permiso de modelo.

## Firma

```python
def list_certificados(request, obra: str=''):
```

## Uso real

`GET /v1/api/certificados/` — response=`List[CertificadoOut]`.

## Ver también

- [Certificado](../../../carga/models/Certificado.md)
