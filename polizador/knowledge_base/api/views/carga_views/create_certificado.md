---
symbol: create_certificado
kind: function
module: api/views/carga_views.py
lines: 1281-1282
signature_hash: sha1:9959797ca223234263697fe825b3dbd9be3d6bd2
authored: true
---

# create_certificado

**Módulo:** `api/views/carga_views.py` (líneas 1281-1282)

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
