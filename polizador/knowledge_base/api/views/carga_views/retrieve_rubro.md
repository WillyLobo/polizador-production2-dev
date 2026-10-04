---
symbol: retrieve_rubro
kind: function
module: api/views/carga_views.py
lines: 1198-1199
signature_hash: sha1:cad3e96f752b5239d43ce54c3fb292df503e68fa
authored: true
---

# retrieve_rubro

**Módulo:** `api/views/carga_views.py` (líneas 1198-1199)

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
