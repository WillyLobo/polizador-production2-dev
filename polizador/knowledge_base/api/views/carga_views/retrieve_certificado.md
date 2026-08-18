---
symbol: retrieve_certificado
kind: function
module: api/views/carga_views.py
lines: 1274-1275
signature_hash: sha1:e120753035925faf757bb5dac4f1bb175cbd4a98
authored: true
---

# retrieve_certificado

**Módulo:** `api/views/carga_views.py` (líneas 1274-1275)

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
