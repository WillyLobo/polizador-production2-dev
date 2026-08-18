---
symbol: retrieve_rubro
kind: function
module: api/views/carga_views.py
lines: 1197-1198
signature_hash: sha1:df13d38650693065c3960e5f3f6d727191f611ce
authored: true
---

# retrieve_rubro

**Módulo:** `api/views/carga_views.py` (líneas 1197-1198)

## Propósito

Devuelve un `CertificadoRubro` puntual por `id` (`get_object_or_404`, 404 si no existe).

## Firma

```python
def retrieve_rubro(request, id: int):
```

## Uso real

`GET /v1/api/rubro/{{id}}/` — response=`CertificadoRubroOut`.

## Ver también

- [CertificadoRubro](../../../carga/models/CertificadoRubro.md)
