---
symbol: create_certificado
kind: function
module: api/views/carga_views.py
lines: 1280-1281
signature_hash: sha1:16334b59cc914d83ba3f1cb4b7a9e17e4d4b64f2
authored: true
---

# create_certificado

**Módulo:** `api/views/carga_views.py` (líneas 1280-1281)

## Propósito

Alta de `Certificado` desde `CertificadoCreate` (`payload.model_dump()` directo a `Certificado.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_certificado(request, payload: CertificadoCreate):
```

## Uso real

`POST /v1/api/certificados/` — response=`CertificadoOut`.

## Ver también

- [Certificado](../../../carga/models/Certificado.md)
