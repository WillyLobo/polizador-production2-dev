---
symbol: delete_financiamiento
kind: function
module: api/views/carga_views.py
lines: 1256-1258
signature_hash: sha1:56fdaecadbe6c7b2c67135ee758e4ec7d33436e3
authored: true
---

# delete_financiamiento

**Módulo:** `api/views/carga_views.py` (líneas 1256-1258)

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
