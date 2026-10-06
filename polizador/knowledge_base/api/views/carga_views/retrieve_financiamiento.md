---
symbol: retrieve_financiamiento
kind: function
module: api/views/carga_views.py
lines: 1235-1236
signature_hash: sha1:bacfba57fd085db01a8b12bf6021516f4cdff4e4
authored: true
---

# retrieve_financiamiento

**Módulo:** `api/views/carga_views.py` (líneas 1235-1236)

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
