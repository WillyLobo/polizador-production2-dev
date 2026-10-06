---
symbol: delete_financiamiento
kind: function
module: api/views/carga_views.py
lines: 1257-1259
signature_hash: sha1:7ec71fa59f77c844b002877951054422221fb0b9
authored: true
---

# delete_financiamiento

**Módulo:** `api/views/carga_views.py` (líneas 1257-1259)

## Propósito

Borrado físico (no soft-delete) de un `CertificadoFinanciamiento` por `id`; devuelve `{"deleted": bool}`.

## Firma

```python
def delete_financiamiento(request, id: int):
```

## Uso real

`DELETE /v1/api/.../{{id}}/`.

## Ver también

- [CertificadoFinanciamiento](../../../carga/models/CertificadoFinanciamiento.md)
