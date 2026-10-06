---
symbol: update_rubro
kind: function
module: api/views/carga_views.py
lines: 1210-1215
signature_hash: sha1:f8c8a2edf5bf99ca596c3a5740a2e0f841606b99
authored: true
---

# update_rubro

**Módulo:** `api/views/carga_views.py` (líneas 1210-1215)

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
