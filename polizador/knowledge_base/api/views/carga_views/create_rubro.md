---
symbol: create_rubro
kind: function
module: api/views/carga_views.py
lines: 1204-1205
signature_hash: sha1:591c085feb655242c4e07387d8d0db38b448acc5
authored: true
---

# create_rubro

**Módulo:** `api/views/carga_views.py` (líneas 1204-1205)

## Propósito

Alta de `CertificadoRubro` desde `CertificadoRubroCreate` (`payload.model_dump()` directo a `CertificadoRubro.objects.create()` — sin lógica de negocio propia acá, la validación vive en el schema ninja/Pydantic).

## Firma

```python
def create_rubro(request, payload: CertificadoRubroCreate):
```

## Uso real

`POST /v1/api/rubros/` — response=`CertificadoRubroOut`.

## Ver también

- [CertificadoRubro](../../../carga/models/CertificadoRubro.md)
