---
symbol: update_certificado
kind: function
module: api/views/carga_views.py
lines: 1286-1291
signature_hash: sha1:f17c3a486a8b096005e7d34b6f3f555daebc7115
authored: true
---

# update_certificado

**Módulo:** `api/views/carga_views.py` (líneas 1286-1291)

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
