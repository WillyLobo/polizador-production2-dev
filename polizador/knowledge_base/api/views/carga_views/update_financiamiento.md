---
symbol: update_financiamiento
kind: function
module: api/views/carga_views.py
lines: 1246-1251
signature_hash: sha1:b901cacba00f028d16d3a95308a7c6fcd8a02724
authored: true
---

# update_financiamiento

**Módulo:** `api/views/carga_views.py` (líneas 1246-1251)

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
