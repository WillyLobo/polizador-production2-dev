---
symbol: retrieve_certificado
kind: function
module: api/views/carga_views.py
lines: 1275-1276
signature_hash: sha1:a92d82949bcb428a44e76019f6639de91f08f376
authored: true
---

# retrieve_certificado

**Módulo:** `api/views/carga_views.py` (líneas 1275-1276)

## Propósito

Devuelve un `Certificado` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_certificado(request, id: int):
```

## Uso real

`GET /v1/api/certificado/{{id}}/` — response=`CertificadoOut`.

## Ver también

- [Certificado](../../../carga/models/Certificado.md)
