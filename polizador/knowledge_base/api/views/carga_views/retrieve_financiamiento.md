---
symbol: retrieve_financiamiento
kind: function
module: api/views/carga_views.py
lines: 1234-1235
signature_hash: sha1:eccc62a83cb01e89b1b7d919a5a326f50c22231d
authored: true
---

# retrieve_financiamiento

**Módulo:** `api/views/carga_views.py` (líneas 1234-1235)

## Propósito

Devuelve un `CertificadoFinanciamiento` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_financiamiento(request, id: int):
```

## Uso real

`GET /v1/api/financiamiento/{{id}}/` — response=`CertificadoFinanciamientoOut`.

## Ver también

- [CertificadoFinanciamiento](../../../carga/models/CertificadoFinanciamiento.md)
