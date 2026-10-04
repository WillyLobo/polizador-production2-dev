---
symbol: list_certificados
kind: function
module: api/views/carga_views.py
lines: 1266-1270
signature_hash: sha1:32b2cccbfcaae7450d6421e5f00fe47ff71df655
authored: true
---

# list_certificados

**Módulo:** `api/views/carga_views.py` (líneas 1266-1270)

## Propósito

Listado paginado (`PerPagePagination`) de `Certificado`, gateado por `require_model_perm(Certificado)` (permiso `view_<modelo>`). Con `?obra=` para acotar a una Obra. El gate por grupo `gciaoperativa_usuarios` se quitó: `view_certificado` cubría exactamente al mismo conjunto de usuarios (ver `verificar_permisos_ui`).

## Firma

```python
def list_certificados(request, obra: str=''):
```

## Uso real

`GET /v1/api/certificados/` — response=`List[CertificadoOut]`.

## Ver también

- [Certificado](../../../carga/models/Certificado.md)
