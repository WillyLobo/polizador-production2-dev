---
symbol: update_certificado
kind: function
module: api/views/carga_views.py
lines: 1287-1292
signature_hash: sha1:b1841c7ecc257305ab574387c7f46581da57c75b
authored: true
---

# update_certificado

**Módulo:** `api/views/carga_views.py` (líneas 1287-1292)

## Propósito

Actualización parcial de un `Certificado` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_certificado(request, id: int, payload: CertificadoUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`CertificadoOut`.

## Ver también

- [Certificado](../../../carga/models/Certificado.md)
