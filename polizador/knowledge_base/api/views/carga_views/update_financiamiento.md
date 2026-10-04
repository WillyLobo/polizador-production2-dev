---
symbol: update_financiamiento
kind: function
module: api/views/carga_views.py
lines: 1247-1252
signature_hash: sha1:8225e1f6591e4e91fa6b44a4f5e00f0c05574bba
authored: true
---

# update_financiamiento

**Módulo:** `api/views/carga_views.py` (líneas 1247-1252)

## Propósito

Actualización parcial de un `CertificadoFinanciamiento` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_financiamiento(request, id: int, payload: CertificadoFinanciamientoUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`CertificadoFinanciamientoOut`.

## Ver también

- [CertificadoFinanciamiento](../../../carga/models/CertificadoFinanciamiento.md)
