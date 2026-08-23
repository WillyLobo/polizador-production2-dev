---
symbol: update_rubro
kind: function
module: api/views/carga_views.py
lines: 1209-1214
signature_hash: sha1:01d6fa1d4d5d6401e05a5018f277234dd9416f27
authored: true
---

# update_rubro

**Módulo:** `api/views/carga_views.py` (líneas 1209-1214)

## Propósito

Actualización parcial de un `CertificadoRubro` (`payload.model_dump(exclude_unset=True)` — solo pisa los campos que vinieron en el payload, `setattr` campo por campo).

## Firma

```python
def update_rubro(request, id: int, payload: CertificadoRubroUpdate):
```

## Uso real

`PUT /v1/api/.../{{id}}/` — response=`CertificadoRubroOut`.

## Ver también

- [CertificadoRubro](../../../carga/models/CertificadoRubro.md)
